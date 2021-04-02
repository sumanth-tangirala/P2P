# PyDash
from pydash.objects import get

# Classes
from Classes.Metadata.Metadata import Metadata

# Helpers
from helpers.file import getChildFilePath
from helpers.piece import getPieceHash


class Downloader:
    def __init__(self, metadata: Metadata, downloadDirectoryPath: str):
        self.metadata = metadata
        self.downloadDirectoryPath = downloadDirectoryPath
        
        # TODO: Single File Case
        fileName = metadata.name
        self.downloadPath = getChildFilePath(downloadDirectoryPath, fileName)
        self.outputFile = open(self.downloadPath, 'wb')
    
    def downloadPiece(self, receivedPiece: bytes, index: int):
        receivedPieceHash = getPieceHash(receivedPiece)
        expectedPieceHash = get(self, ['metadata', 'pieceHashes', index])
        
        if receivedPieceHash != expectedPieceHash:
            raise ValueError('Hash mismatch')
        
        self.outputFile.write(receivedPiece)
    
    def closeFile(self):
        self.outputFile.close()
