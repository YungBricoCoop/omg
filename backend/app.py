import asyncio
import json
import secrets
import string
from typing import Dict

from fastapi import FastAPI, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from starlette.config import Config
from utils.utils import Logger, avg, analyze_mail_domain, analyze_attachements, analyze_links, analyze_subject_and_body
from utils.MailServer import MailServer

# general setup
config = Config('.env')
logger = Logger(__name__).logger

app = FastAPI()
app.add_middleware(
	CORSMiddleware,
	allow_origins=['*'],
	allow_credentials=True,
	allow_methods=['*'],
	allow_headers=['*'],
)

ID_LENGTH = config('ID_LENGTH', cast=int)
SAFE_BROWSING_API_KEY = config('SAFE_BROWSING_API_KEY')
OPENAI_API_KEY = config('OPENAI_API_KEY')

connections: Dict[str, WebSocket] = {}
disposable_domains = []

async def send(id, data):
	if id in connections:
		await connections[id].send_text(json.dumps(data))
		return True
	else:
		logger.warning(f"Socket {id} not found")
		return False

async def analyze_mail(data):
	id = data['id']
	# ---------- STEP 1 --------- : MAIL RECEIVED
	status = {
		"step": 1,
	}
	if not await send(id, status): return
	# /X--------- STEP 1 --------X/

	# ---------- STEP 2 --------- : ANALYZE SENDER, ATTACHMENTS, LINKS 
	sender_oddness = analyze_mail_domain(disposable_domains, data['sender'])
	attachments_analysis = analyze_attachements(data['attachments'])
	links_analysis = analyze_links(SAFE_BROWSING_API_KEY, data['links'])

	status = {
		"step": 2,
		"sender" : data['sender'],
		"sender_oddness": sender_oddness,
		"attachments": attachments_analysis['attachments'],
		"attachments_oddness": attachments_analysis['oddness'],
		"links": links_analysis['links'],
		"links_oddness": links_analysis['oddness']
	}
	
	if not await send(id, status): return
	# /X--------- STEP 2 --------X/

	# ---------- STEP 3 --------- : ANALYZE SUBJECT AND BODY
	subject_and_body_analysis = analyze_subject_and_body(OPENAI_API_KEY, data['subject'], data['body'])
	
	status = {
		**status,
		"step": 3,
		"subject": data['subject'],
		"subject_oddness": subject_and_body_analysis['subject'],
		"body": data['body'],
		"body_oddness": subject_and_body_analysis['body']
	}

	if not await send(id, status): return
	# /X--------- STEP 3 --------X/

# setup mail server
mail_server = MailServer(analyze_mail, config, logger)

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
			await asyncio.sleep(1)
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
	asyncio.create_task(mail_server.listen())

@app.exception_handler(Exception)
async def handle_generic_error(request, exc):
    logger.error(str(exc))