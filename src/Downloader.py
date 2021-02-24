# PyDash
from pydash.objects import get as _get

# Classes
from Metadata import Metadata

# Helpers
from helpers.piece import getPieceHash

class Downloader:
	def __init__(self, metadata: Metadata, downloadDirectoryPath):
		self.metadata = metadata
		self.downloadDirectoryPath = downloadDirectoryPath
		
		# TODO: Single File Case
		fileName = metadata.name
		self.downloadPath = '{}/{}'.format(downloadDirectoryPath, fileName)
		self.outputFile = open(self.downloadPath, 'wb')
		
	def downloadPiece(self, receivedPiece, index):
		receivedPieceHash = getPieceHash(receivedPiece)
		expectedPieceHash = _get(self, ['metadata', 'pieceHashes', index])
		
		if receivedPieceHash != expectedPieceHash:
			raise ValueError('Hash mismatch')

		self.outputFile.write(receivedPiece)
		
	def closeFile(self):
		self.outputFile.close()
