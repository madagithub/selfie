import os
import psutil

import logging
from logging.handlers import RotatingFileHandler

class Log:

	SEPARATOR = '|'

	logger = None
	exhibitName = ''

	@staticmethod
	def init(logFilePath, exhibitName):
		Log.exhibitName = exhibitName

		logging.basicConfig(filename=logFilePath, filemode='a', level=logging.INFO)

		handler = RotatingFileHandler(logFilePath, maxBytes=37500, backupCount=100)
		Log.logger = logging.getLogger("Rotating Log")
		formatter = logging.Formatter('%(asctime)s.%(msecs)03d|%(levelname)s|%(message)s', '%Y-%m-%d %H:%M:%S')
		handler.setFormatter(formatter)
		Log.logger.propagate = False
		Log.logger.addHandler(handler)

	@staticmethod
	def getLogger():
		return Log.logger

	@staticmethod
	def prepareLogMessage(message, parts):
		process = psutil.Process(os.getpid())
		memoryUsage = int(process.memory_info().rss / float(2 ** 20))
		fullMessage = Log.exhibitName + Log.SEPARATOR + str(memoryUsage) + 'MB' + Log.SEPARATOR + message
		if len(parts) > 0:
			fullMessage += (Log.SEPARATOR + Log.SEPARATOR.join(parts))

		return fullMessage

	@staticmethod
	def info(message, *parts):
		Log.logger.info(Log.prepareLogMessage(message, list(parts)))

	@staticmethod
	def error(message, *parts):
		Log.logger.error(Log.prepareLogMessage(message, list(parts)))

