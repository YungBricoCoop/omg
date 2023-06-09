import asyncio
import imaplib
import json
import secrets
import string
from typing import Dict

from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from starlette.config import Config
from utils import Logger, avg, mail_to_dict, is_disposable, mail_to_dict, analyze_attachements, analyze_links, analyze_subject_and_body

# setup logger
logger = Logger(__name__).logger

app = FastAPI()
app.add_middleware(
	CORSMiddleware,
	allow_origins=['*'],
	allow_credentials=True,
	allow_methods=['*'],
	allow_headers=['*'],
)

config = Config('.env')

ID_LENGTH = config('ID_LENGTH', cast=int)
SAFE_BROWSING_API_KEY = config('SAFE_BROWSING_API_KEY')
OPENAI_API_KEY = config('OPENAI_API_KEY')

mail = imaplib.IMAP4_SSL(config('MAIL_SERVER'), config('MAIL_IMAP_PORT'))
mail.login(config('MAIL_USERNAME'), config('MAIL_PASSWORD'))

connections: Dict[str, WebSocket] = {}
disposable_domains = []


async def check_mail():
	logger.info("Checking mail...")
	while True:
		mail.select('inbox')
		result, data = mail.uid('search', None, "UNSEEN")
		email_ids = data[0].split()
		for e_id in email_ids:
			logger.info(f"Found email with id {e_id}")
			oddness = {
				"sender": 0,
				"attachments": 0,
				"links": 0,
				"subject": 0,
				"body": 0,
			}

			# get raw email data
			result, email_data = mail.uid('fetch', e_id, '(BODY[])')
			raw_email = email_data[0][1]

			# delete the mail
			if raw_email:
				mail.uid('store', e_id, '+FLAGS', '\\Deleted')
				mail.expunge()
			
			# extract the data
			email_dict = mail_to_dict(raw_email, ID_LENGTH)

			# ---------- STEP 1 --------- : MAIL RECEIVED
			id = email_dict['id']	
			if id not in connections: 
				# skip if the id is not in the connections
				logger.warning(f"Socket {id} not found")
				continue

			await connections[id].send_text(json.dumps({
				"step": 1,
			}))
			# /X--------- STEP 1 --------X/
			
			#  ---------- STEP 2 --------- : ANALYZE SENDER, ATTACHMENTS, LINKS 
			if is_disposable(disposable_domains, email_dict['from']):
				oddness['sender'] = 100

			attachments = analyze_attachements(raw_email)
			oddness ["attachments"]= avg([attachment['oddness'] for attachment in attachments]) if attachments else 0

			links = analyze_links(SAFE_BROWSING_API_KEY, email_dict['links'])
			oddness["link"] = avg([link['oddness'] for link in links]) if links else 0
			
			await connections[id].send_text(json.dumps({
				"step": 2,
				"sender": email_dict['from'],
				"sender_oddness" : oddness['sender'],
				"links": links,
				"links_oddness" : oddness['links'], 
				"attachments": attachments,
				"attachments_oddness": oddness['attachments'],
			}))
			# /X--------- STEP 2 --------X/

			#  ---------- STEP 3 --------- : ANALYZE SUBJECT, BODY	
			subject_and_body = analyze_subject_and_body(OPENAI_API_KEY, email_dict['subject'], email_dict['body_text'])
			oddness["subject"] = subject_and_body['subject']
			oddness["body"] = subject_and_body['body']
			
			data = {
				"step": 3,
				"sender": email_dict['from'],
				"sender_oddness" : oddness['sender'],
				"subject": email_dict['subject'],
				"subject_oddness": oddness['subject'],
				"links": links,
				"links_oddness" : oddness['links'],
				"body": email_dict['body_text'],
				"body_oddness": oddness['body'],
				"attachments": attachments,
				"attachments_oddness": oddness['attachments'],
				"oddness": max(oddness.values())
			}

			await connections[id].send_text(json.dumps(data))
			# /X--------- STEP 3 --------X/

		# wait 10 seconds before checking again
		await asyncio.sleep(10)


@app.get("/id")
async def get_id():
	alphabet = string.ascii_letters + string.digits
	return ''.join(secrets.choice(alphabet) for i in range(ID_LENGTH))

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
	await websocket.accept()
	connections[client_id] = websocket
	try:
		while True:
			data = await websocket.receive_text()
	except Exception as e:
		logger.error(f"Error occurred: {e}")
	finally:
		del connections[client_id]

@app.on_event("startup")
async def startup_event():
	logger.info("Starting up...")
	global disposable_domains
	with open('./data/disposable_email_domains.txt') as file:
		disposable_domains = set(line.strip() for line in file)	
	asyncio.create_task(check_mail())

@app.exception_handler(Exception)
async def handle_generic_error(request, exc):
    logger.error(str(exc))