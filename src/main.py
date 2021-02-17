from Metadata import Metadata
from Seeder import Seeder
from Downloader import Downloader

PROJECT_PATH = '/Users/tangiralasumanth/All Stuff/Programming Stuff/P2P'

INPUT_TRANSFER_PATH = '{}/TrialFiles/inputTrial/SWTM-2088_Atlassian-Git-Cheatsheet.pdf'.format(PROJECT_PATH)
OUTPUT_TRANSFER_PATH = '{}/TrialFiles/outputTrial'.format(PROJECT_PATH)

if __name__ == "__main__":
	metadata = Metadata(INPUT_TRANSFER_PATH)
	seeder = Seeder(INPUT_TRANSFER_PATH)
	downloader = Downloader(metadata=metadata, downloadDirectoryPath=OUTPUT_TRANSFER_PATH)
	
	# TODO: Simulation
	pieceSize = metadata.pieceSize
	for pieceIndex in range(metadata.numberOfPieces):
		piece = seeder.getOutput(pieceSize)
		downloader.downloadPiece(piece, pieceIndex)
		
	downloader.closeFile()
	seeder.closeFile()
