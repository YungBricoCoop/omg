import json
import logging
import re
from logging.handlers import TimedRotatingFileHandler

import openai
from pysafebrowsing import SafeBrowsing


class Logger:
	def __init__(self, name: str):
		FILE_FORMAT = "%d-%m-%Y.log"
		FORMAT = "[%(levelname)s] %(asctime)s %(message)s"
		ROTATION = "midnight"
		RETENTION = 7
		
		self.logger = logging.getLogger(name)
		self.logger.setLevel(logging.INFO)
		self.formatter = logging.Formatter(FORMAT, datefmt='%d.%m.%Y %H:%M:%S')
		self.file_handler = TimedRotatingFileHandler(f"logs/app.log", when=ROTATION, backupCount=RETENTION)
		self.file_handler.suffix = FILE_FORMAT
		self.file_handler.setLevel(logging.INFO)
		self.file_handler.setFormatter(self.formatter)
		self.logger.addHandler(self.file_handler)
		
	def log(self, message: str):
		self.logger.info(message)


def avg(l: list) -> float:
	return sum(l) / len(l) if l else 0


def extract_sender_from_body(body: str , sender: str) -> str:
	if "<" in sender and ">" in sender:
		sender = sender.split("<")[1].split(">")[0]
	print(body)
	email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
	email_match = re.search(email_pattern, body)
	sender = ""
	if email_match:
		print(email_match.group())
		sender = email_match.group()
	
	return sender

def extract_links_from_body(body: str) -> list:
	links = []
	links_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
	links = re.findall(links_pattern, body)

	return links

def extract_attachments_from_body(email_message) -> list:
	attachments = []
	for part in email_message.iter_parts():
			if part.get_content_disposition() == 'attachment':
				attachments.append(part.get_filename())
	return attachments

def analyze_mail_domain(disposable_domains, mail: str) -> bool:
	if not mail: return 0
	if '@' not in mail: return 0
	domain = mail.split('@')[1].strip()
	return 100 if domain in disposable_domains else 0

def analyze_attachements(attachments: list) -> dict:
	extensions = {
		'exe': 100,
		'pif': 100,
		'scr': 100,
		'bat': 100,
		'docm': 90,
		'xlsm': 90,
		'pptm': 90,
		'js': 90,
		'vbs': 90,
		'ps1': 90,
		'jar': 85,
		'class': 85,
		'swf': 85,
		'zip': 75,
		'rar': 75,
		'7z': 75,
		'pdf': 60,
		'docx': 30,
		'xlsx': 30,
		'pptx': 30,
		'txt': 5,
		'png': 0,
		'jpg': 0,
		'jpeg': 0,
	}
	for attachment in attachments:
		ext = attachment.split('.')[-1].lower()
		oddness = extensions.get(ext, 0)

		attachments.append({
			"name": attachment,
			"oddness": oddness,
		})
		
	oddness = avg([attachment['oddness'] for attachment in attachments])

	return {
		"oddness": oddness,
		"attachments": attachments,
	}
	
def analyze_links(api_key: str, links : list) -> dict:
	if not links: return {
		"oddness": 0,
		"links": [],
	}
	safe_browsing_api = SafeBrowsing(api_key)
	
	# verify the links to get the level of oddness
	result = safe_browsing_api.lookup_urls(links)
	if not result: return {
		"oddness": 0,
		"links": [],
	}
	
	links =  [{
		"link": link,
		"oddness": 100 if result[link]['malicious'] else 0,
		"threats": result[link]['threats'] if 'threats' in result[link] else [],
	} for link in result.keys()]

	oddness = avg([link['oddness'] for link in links])

	return {
		"oddness": oddness,
		"links": links,
	}

def analyze_subject_and_body(api_key: str, subject: str, body: str) -> dict:
	openai.api_key = api_key
	
	# replace emails username and links path by placeholders to avoid data leakage
	email_pattern = r'([\w\.-]+)@([\w\.-]+\.[a-zA-Z]{2,}(?:\.[a-zA-Z]{2,})*)'
	body = re.sub(email_pattern, r'xxx@\2', body)

	url_pattern = r'(http|https)\:\/\/[a-zA-Z0-9\-\.]+\.[a-zA-Z]{2,}(?:\.[a-zA-Z]{2,})*(\/\S*)?'
	body = re.sub(url_pattern, lambda x: re.search(r'[a-zA-Z0-9\-\.]+\.[a-zA-Z]{2,}(?:\.[a-zA-Z]{2,})*', x.group()).group(), body)
	
	# create the prompt
	messages = [
		{"role" : "system", "content" : "You are a cybersecurity expert. You are tasked with analyzing a suspicious email."},
		{"role" : "user", 
  		 "content" : f"""
		Given the following email, return a value between 0 and 100 representing the threat level of the email. Links and email are replaced by placeholders to avoid data leakage.
		Do not include any explanations, only provide a  RFC8259 compliant JSON response  following this format without deviation : 
		{{
			"subject": 0,
			"body": 0,
		}}

		Subject: {subject}
		Body: {body}"""}]

	completion = openai.ChatCompletion.create(
		model="gpt-3.5-turbo",
		messages=messages
	)
	try:
		# convert the response to a dict
		response = completion.choices[0].message.content.strip()
		dict_response = json.loads(response)
	
	except:
		dict_response = {
			"subject": 0,
			"body": 0,
		}
	return dict_response