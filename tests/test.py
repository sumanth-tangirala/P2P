from pathlib import Path

# Classes
from Classes.Metadata.Metadata import Metadata
from Classes.Seeder.Seeder import Seeder
from Classes.Downloader.Downloader import Downloader

# Helpers
from Classes.Metadata.MetadataHelpers import getFileIdToFilePathMapping

PROJECT_PATH = '/Users/tangiralasumanth/All Stuff/Programming Stuff/P2P/tests'

INPUT_TRANSFER_PATH = '{}/TrialFiles/metadata.json'.format(PROJECT_PATH)
BASE_INPUT_TRANSFER_PATH = '{}/TrialFiles'.format(PROJECT_PATH)
OUTPUT_TRANSFER_PATH = '{}/TrialFiles/outputTrial'.format(PROJECT_PATH)

if __name__ == "__main__":
    path = Path(INPUT_TRANSFER_PATH)
    baseInputPath = Path(BASE_INPUT_TRANSFER_PATH)
    outputPath = Path(OUTPUT_TRANSFER_PATH)
    print('Creating metadata')
    metadata = Metadata(path)
    print('Metadata created. Initializing Seeder and Downloader')
    fileIdVsFilePath = getFileIdToFilePathMapping(metadata.structure)
    seeder = Seeder(metadata=metadata, sourcePath=baseInputPath, fileIdVsFilePath=fileIdVsFilePath)
    pieceBitmap = [False] * metadata.numberOfPieces
    downloader = Downloader(metadata=metadata, downloadDirectoryPath=outputPath, pieceBitMap=pieceBitmap, fileIdVsFilePath=fileIdVsFilePath)
    for pieceIndex in range(metadata.numberOfPieces):
        print('{}/{}'.format(pieceIndex+1, metadata.numberOfPieces))
        piece = seeder.getPiece(pieceIndex)
        downloader.downloadPiece(piece, pieceIndex)
