import asyncio
import imaplib
from email.parser import BytesParser
from email.policy import default

from bs4 import BeautifulSoup
from utils.utils import extract_sender_from_body, extract_links_from_body, extract_attachments_from_body


class MailServer:
	def __init__(self, callback, config, logger):
		self.callback = callback
		self.config = config
		self.logger = logger
		self.id_length = config('ID_LENGTH', cast=int, default=8)
		self.fetch_delay = config('FETCH_DELAY', cast=int ,default=10)
		self.mail = None
		self.login()
		self.disposable_domains = []
	
	def login(self):
		self.mail = imaplib.IMAP4_SSL(self.config('MAIL_SERVER'), self.config('MAIL_IMAP_PORT'))
		self.mail.login(self.config('MAIL_USERNAME'), self.config('MAIL_PASSWORD'))

	async def listen(self):
		self.logger.info("Listening for incomming mails...")
		while True:
			try:
				self.mail.select('inbox')
				_, data = self.mail.uid('search', None, "UNSEEN")
				email_ids = data[0].split()
				for e_id in email_ids:
					await self.process_mail(e_id)

			except imaplib.IMAP4.error as e:
				self.logger.error(f"IMAP4 error: {str(e)}, reconnecting...")
				self.login()
			
			await asyncio.sleep(self.fetch_delay)
				
	async def process_mail(self, e_id):
		self.logger.info(f"Found email with id {e_id}")

		# get raw email data
		_, mail_data = self.mail.uid('fetch', e_id, '(BODY[])')
		raw_mail = mail_data[0][1]

		# delete the mail
		if raw_mail:
			self.mail.uid('store', e_id, '+FLAGS', '\\Deleted')
			self.mail.expunge()
		
		# extract the data
		mail_data = self.mail_to_dict(raw_mail)

		# call the callback
		await self.callback(mail_data)


	def get_body(self, email_message):
		if email_message.is_multipart():
			for part in email_message.iter_parts():
				if part.get_content_type() in ['text/plain', 'text/html']:
					return part.get_content()
				elif part.get_content_type().startswith('multipart/'):
					return self.get_body(part)
		
		return email_message.get_content()

	def mail_to_dict(self, raw_email: bytes) -> dict:
		email_message = BytesParser(policy=default).parsebytes(raw_email)

		# extract the subject
		subject = email_message.get('Subject', '')
		
		# get the id from the subject
		id = subject.strip()[:self.id_length]

		# remove the id from the subject
		subject = subject[self.id_length:].strip()

		# extract the body
		body = self.get_body(email_message)

		# get body without tags
		body_text = BeautifulSoup(body, "html.parser").text	

		# extract the sender from the body
		from_sender = email_message.get('From')
		from_sender = extract_sender_from_body(body , from_sender)
		
		# extract the links from the body
		links = extract_links_from_body(body)

		# extract the attachments from the body
		attachments = extract_attachments_from_body(email_message)


		return {
			"id": id,
			"body": body,
			"body_text": body_text,
			"subject": subject,
			"sender": from_sender,
			"links": links,
			"attachments": attachments
		}