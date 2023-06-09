import asyncio
import imaplib
import secrets
import string
from typing import Dict

from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from starlette.config import Config

from utils import Logger


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