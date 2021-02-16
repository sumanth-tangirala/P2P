import os

def getTransferSize(transferPath: str):
	fileStats = os.stat(transferPath)
	return fileStats.st_size


def getFileNameFromPath(path: str):
	try:
		return path.split('/')[-1]
	except AttributeError:
		raise ValueError('Incorrect Path')
