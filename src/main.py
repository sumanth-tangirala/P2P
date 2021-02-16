from src.Metadata import Metadata
from src.Seeder import Seeder
from src.Downloader import Downloader

INPUT_TRANSFER_PATH = '../TrialFiles/inputTrial/SWTM-2088_Atlassian-Git-Cheatsheet.pdf'
OUTPUT_TRANSFER_PATH = '../TrialFiles/outputTrial'

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
