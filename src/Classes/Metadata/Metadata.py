from operator import itemgetter
from pathlib import Path

# Classes
from .HelperClasses.Structure import Structure

# Helpers
from helpers.file import getTransferSize
from helpers.piece import getPieceDetails

# Constants
from constants.appConstants import EMPTY_TUPLE


class Metadata:
    def __init__(self, transferPath: Path):
        if not transferPath.exists():
            raise ValueError('No such file or directory exists - {}'.format(transferPath.absolute()))
        
        transferSize = getTransferSize(transferPath)
        pieceSize, numberOfPieces = itemgetter('pieceSize', 'numberOfPieces')(getPieceDetails(transferSize))
        
        self.transferPath = transferPath
        self.transferSize = transferSize
        self.name = transferPath.name
        self.numberOfPieces = numberOfPieces
        self.pieceSize = pieceSize
        self.pieceHashes = EMPTY_TUPLE
        self.structure = Structure(transferPath.name, transferPath.is_file())
    
    def setPieceHashes(self, pieceHashes: tuple):
        self.pieceHashes = pieceHashes
    
    def populatePieceDetails(self):
        if self.transferPath.is_dir():
            from Classes.Metadata.MetadataHelpers import populateDirectoryPieceDetails
            return populateDirectoryPieceDetails(self)
        if self.transferPath.is_file():
            from Classes.Metadata.MetadataHelpers import populateFilePieceDetails
            return populateFilePieceDetails(self)
