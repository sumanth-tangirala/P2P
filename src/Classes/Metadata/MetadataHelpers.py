from pathlib import Path
import math

# Classes
from .HelperClasses.Structure import Structure
from .HelperClasses.PieceDetails import PieceDetails

# Helpers
from helpers.piece import getPieceHash, getPieceGenerator

# Constants
from constants.appConstants import EMPTY_STRING


def getDirectoryPieceDetails(descendantPaths: tuple, descendantFilePathsVsId: dict, pieceSize: int, numberOfPieces: int):
    pieceDetailsList = list()
    pieceGenerator = getPieceGenerator(descendantPaths, descendantFilePathsVsId, pieceSize, numberOfPieces)
    for pieceIndex, (piece, pieceFileByteIndicesList) in enumerate(pieceGenerator):
        pieceDetailsList.append(PieceDetails(
            pieceHash=getPieceHash(piece),
            pieceFileByteIndicesList=pieceFileByteIndicesList
        ))
    return tuple(pieceDetailsList)


def getDirectoryStructure(directoryPath: Path, descendantFilePathsVsId: dict):
    childrenStructures = list()
    for child in directoryPath.iterdir():
        isChildFile = child.is_file()
        childStructure = Structure(
            name=child.name,
            isFile=isChildFile,
            fileId=descendantFilePathsVsId[str(child.absolute())] if isChildFile else None,
            childrenStructures=getDirectoryStructure(child, descendantFilePathsVsId) if not isChildFile else None,
        )
        childrenStructures.append(childStructure)

    
    return tuple(childrenStructures)

def getFileIdToFilePathMapping(structure: Structure, parentPathString: str = None):
    fileIdVsFilePath = dict()
    currentPath = structure.name if not parentPathString else '{}/{}'.format(parentPathString, structure.name)
    if structure.isFile:
        fileIdVsFilePath[structure.fileId] = currentPath
    else:
        for child in structure.children:
            fileIdVsFilePath.update(getFileIdToFilePathMapping(child, currentPath))
    
    return fileIdVsFilePath
