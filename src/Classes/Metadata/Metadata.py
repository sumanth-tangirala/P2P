from operator import itemgetter
from pathlib import Path

# Classes
from .HelperClasses.Structure import Structure

# Helpers
from helpers.file import getTransferSize, getSortedDescendantFilePathStrings, getFilePathToFileIdMapping
from helpers.piece import getPieceDetails
from .MetadataHelpers import getDirectoryPieceDetails, getDirectoryStructure

def _getPieceAndStructureDetails(transferPath: Path, pieceSize: int, numberOfPieces: int):
    descendantFilePaths = getSortedDescendantFilePathStrings(transferPath)
    descendantFilePathsVsId = getFilePathToFileIdMapping(descendantFilePaths)
    isTransferTargetFile = transferPath.is_file()
    
    pieceDetailsList = getDirectoryPieceDetails(descendantFilePaths, descendantFilePathsVsId, pieceSize, numberOfPieces)
    structure = Structure(
        name=transferPath.name,
        isFile=isTransferTargetFile,
        fileId=descendantFilePathsVsId[str(transferPath.absolute())] if isTransferTargetFile else None,
        childrenStructures=getDirectoryStructure(transferPath, descendantFilePathsVsId) if not isTransferTargetFile else None,
    )
    
    return structure, pieceDetailsList


class Metadata:
    def __init__(self, transferPath: Path):
        if not transferPath.exists():
            raise ValueError('No such file or directory exists - {}'.format(transferPath.absolute()))
        
        transferSize = getTransferSize(transferPath)
        pieceSize, numberOfPieces = getPieceDetails(transferSize)
        structure, pieceDetailsList = _getPieceAndStructureDetails(transferPath, pieceSize, numberOfPieces)
        
        self.name = transferPath.name
        self.transferSize = transferSize
        self.pieceSize = pieceSize
        self.numberOfPieces = numberOfPieces
        self.structure = structure
        self.pieceDetailsList = pieceDetailsList
        
    def toJSON(self):
        return {
            "transferSize": self.transferSize,
            "name": self.name,
            "numberOfPieces": self.numberOfPieces,
            "pieceSize": self.pieceSize,
            "structure": self.structure.toJSON(),
            "pieceDetailsList": list(map(lambda pieceDetails: pieceDetails.toJSON(), self.pieceDetailsList)),
        }
