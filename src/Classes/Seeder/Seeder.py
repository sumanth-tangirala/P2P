from pathlib import Path

# Classes
from Classes.Metadata.Metadata import Metadata

# Helpers
from helpers.file import getFilePathString, getSortedDescendantFilePathStrings


# TODO: Remove path and make it either download or source path
# TODO: Handle partial fetch state later
class Seeder:
    def __init__(self, metadata: Metadata, path: str, isFirstSeeder: bool):
        self.pieceVsFetchState = [True] * metadata.numberOfPieces if isFirstSeeder else []  # Write function to check status
        self.metadata = metadata
        self.path = Path(path)
        filePathsToTransfer = (
            getFilePathString(self.path)) if self.path.is_file() else getSortedDescendantFilePathStrings(self.path)
    
    def getOutput(self, pieceSize: int):
        return self.inputFile.read(pieceSize)
    
    def closeFile(self):
        self.inputFile.close()
