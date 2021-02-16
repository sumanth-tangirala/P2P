import os

# Helpers
from src.helpers.file import getFileNameFromPath, getTransferSize
from src.helpers.piece import getPieceHash, getPieceDetails


class Metadata:
	def __init__(self, transferPath: str):
		transferSize = getTransferSize(transferPath)
		[pieceSize, numberOfPieces] = getPieceDetails(transferSize)
		self.transferSize = transferSize
		self.name = getFileNameFromPath(transferPath)
		self.numberOfPieces = numberOfPieces
		self.pieceSize = pieceSize
		self.pieceHashes = list()
	
	def populatePieceDetails(self, transferPath: str):
		if os.path.isdir(transferPath):
			return
		with open(transferPath, 'rb') as file:
			piece = file.read(self.pieceSize)
			while len(piece) > 0:
				self.pieceHashes.append(getPieceHash(piece))
				
				piece = file.read(self.pieceSize)
