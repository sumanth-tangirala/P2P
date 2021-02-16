class Seeder:
	def __init__(self, transferPath: str):
		self.inputFile = open(transferPath, 'rb')
	
	def getOutput(self, pieceSize: int):
		return self.inputFile.read(pieceSize)
	
	def closeFile(self):
		self.inputFile.close()
