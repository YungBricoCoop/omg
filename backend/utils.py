import logging
from logging.handlers import TimedRotatingFileHandler

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
