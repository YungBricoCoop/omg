import logging
import re
from email.parser import BytesParser
from email.policy import default
from logging.handlers import TimedRotatingFileHandler

from bs4 import BeautifulSoup


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
