from pathlib import Path

from Classes.Metadata.Metadata import Metadata
from Classes.Seeder.Seeder import Seeder
from Classes.Downloader.Downloader import Downloader

PROJECT_PATH = '/Users/tangiralasumanth/All Stuff/Programming Stuff/P2P'

INPUT_TRANSFER_PATH = '{}/TrialFiles/inputTrial/directory'.format(PROJECT_PATH)
OUTPUT_TRANSFER_PATH = '{}/TrialFiles/outputTrial'.format(PROJECT_PATH)

if __name__ == "__main__":
    path = Path(INPUT_TRANSFER_PATH)
    metadata = Metadata(path)
    metadata.populatePieceDetails()
    seeder = Seeder(
        metadata=metadata,
        path=INPUT_TRANSFER_PATH,
        isFirstSeeder=True,
    )
    # downloader = Downloader(metadata=metadata, downloadDirectoryPath=OUTPUT_TRANSFER_PATH)
    #
    # # TODO: Simulation
    # pieceSize = metadata.pieceSize
    # for pieceIndex in range(metadata.numberOfPieces):
    # 	piece = seeder.getOutput(pieceSize)
    # 	downloader.downloadPiece(piece, pieceIndex)
    #
    # downloader.closeFile()
    # seeder.closeFile()
