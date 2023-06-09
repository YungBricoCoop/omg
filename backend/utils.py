import logging
import re
from email.parser import BytesParser
from email.policy import default
from logging.handlers import TimedRotatingFileHandler

from bs4 import BeautifulSoup
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


def get_body(email_message):
	if email_message.is_multipart():
		for part in email_message.iter_parts():
			if part.get_content_type() in ['text/plain', 'text/html']:
				return part.get_content()
			elif part.get_content_type().startswith('multipart/'):
				return get_body(part)
	
	return email_message.get_content()

def mail_to_dict(raw_email: bytes, id_length: int) -> dict:
	email_message = BytesParser(policy=default).parsebytes(raw_email)

	# extract the subject
	subject = email_message.get('Subject')
	if subject is None:
		raise ValueError("The email doesn't have a 'Subject' field")
	
	# get the id from the subject
	id = subject.strip()[:id_length]

	# remove the id from the subject
	subject = subject[id_length:].strip()

	# extract the body
	body = get_body(email_message)

	# get body without tags
	body_text = BeautifulSoup(body, "html.parser").text	

	# set default sender to the one that sent the email (just the email)
	from_sender = email_message.get('From')
	if "<" in from_sender and ">" in from_sender:
		from_sender = from_sender.split("<")[1].split(">")[0]
	
	# extract the sender by using the first email found in the body
	email_pattern = re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b')
	email_match = re.search(email_pattern, body)
	if email_match:
		from_sender = email_match.group()
	
	links = []
	# extract the links from the body
	links_pattern = r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+'
	links = re.findall(links_pattern, body)


	return {
		"id": id,
		"body": body,
		"body_text": body_text,
		"subject": subject,
		"from": from_sender,
		"links": links,
	}

def avg(l: list) -> float:
	return sum(l) / len(l) if l else 0

def is_disposable(disposable_domains, email: str) -> bool:
	domain = email.split('@')[1].strip()
	return domain in disposable_domains

def analyze_attachements(raw_email: bytes) -> dict:
	email_message = BytesParser(policy=default).parsebytes(raw_email)
	attachments = []
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
	for part in email_message.iter_parts():
		if part.get_content_disposition() == 'attachment':
			ext = part.get_filename().split('.')[-1].lower()
			oddness = extensions.get(ext, 0)

			attachments.append({
				"name": part.get_filename(),
				"oddness": oddness,
			})

	return attachments
	
def analyze_links(api_key: str, links : list) -> dict:
	if not links: return []
	safe_browsing_api = SafeBrowsing(api_key)
	
	# verify the links to get the level of oddness
	result = safe_browsing_api.lookup_urls(links)
	if not result: return []
	
	return [{
		"link": link,
		"oddness": 100 if result[link]['malicious'] else 0,
		"threats": result[link]['threats'] if 'threats' in result[link] else [],
	} for link in result.keys()]