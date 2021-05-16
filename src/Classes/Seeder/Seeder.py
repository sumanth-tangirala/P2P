from pathlib import Path

# PyDash
from pydash.objects import get

# Helpers
from Classes.Seeder.SeederHelpers import getInitialPieceBitmap, getPieceFromFileByteIndices


# TODO: Remove path and make it either download or source path
# TODO: Make it read json metadata rather than actual metadata
class Seeder:
    def __init__(self, metadata, sourcePath: Path, fileIdVsFilePath: dict):
        self._pieceBitmap = getInitialPieceBitmap(metadata, sourcePath, fileIdVsFilePath)
        self._metadata = metadata
        self._sourcePath = sourcePath
        self._fileIdVsFilePath = fileIdVsFilePath
    
    def getPiece(self, pieceIndex: int):
        if not self._pieceBitmap[pieceIndex]:
            # TODO: Handle this situation
            return None
        pieceFileIndices = get(self._metadata, ['pieceDetailsList', pieceIndex, 'pieceFileByteIndicesList'])
        return getPieceFromFileByteIndices(pieceFileIndices, self._sourcePath, self._fileIdVsFilePath)
