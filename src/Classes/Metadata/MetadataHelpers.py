from pathlib import Path

# Classes
from .HelperClasses.PieceIndicesRange import PieceIndicesRange
from .HelperClasses.Structure import Structure
from .Metadata import Metadata

# Helpers
from helpers.file import getSortedDescendantFilePathStrings, getFilePathString
from helpers.piece import getPieceHash, getPieceIndexValue


def populateDirectoryPieceHashes(metadata: Metadata, descendantPaths: tuple):
    currentDescendantIndex = -1
    currentDescendantFile = None
    pieceIndex = None
    piece = None
    descendantVsPieceIndices = {}
    pieceHashes = list()
    
    def updateToNextCurrentDescendant(currentPieceIndex: int, currentByteIndex: int):
        nonlocal currentDescendantIndex
        nonlocal currentDescendantFile
        
        if currentDescendantFile is not None:
            currentFilePath = descendantPaths[currentDescendantIndex]
            descendantVsPieceIndices[currentFilePath].setEnd(getPieceIndexValue(currentPieceIndex, currentByteIndex))
            currentDescendantFile.close()
        
        currentDescendantIndex = currentDescendantIndex + 1
        nextDescendantPath = descendantPaths[currentDescendantIndex]
        currentDescendantFile = open(nextDescendantPath, 'rb')
        descendantVsPieceIndices[nextDescendantPath] = PieceIndicesRange(
            start=getPieceIndexValue(currentPieceIndex, currentByteIndex + 1))
    
    updateToNextCurrentDescendant(0, -1)
    for pieceIndex in range(metadata.numberOfPieces):
        piece = currentDescendantFile.read(metadata.pieceSize)
        while len(piece) < metadata.pieceSize and currentDescendantIndex < len(descendantPaths) - 1:
            updateToNextCurrentDescendant(pieceIndex, len(piece) - 1)
            piece = piece + currentDescendantFile.read(metadata.pieceSize - len(piece))
        if len(piece) == 0:
            break
        pieceHashes.append(getPieceHash(piece))
    
    metadata.setPieceHashes(tuple(pieceHashes))
    
    finalFilePath = descendantPaths[currentDescendantIndex]
    descendantVsPieceIndices[finalFilePath].setEnd(getPieceIndexValue(pieceIndex, len(piece) - 1))
    currentDescendantFile.close()
    return descendantVsPieceIndices


def getDirectoryStructure(directoryPath: Path, filePathsVsPieceIndices: dict):
    childrenStructures = list()
    
    for child in directoryPath.iterdir():
        childStructure = Structure(
            name=child.name,
            isFile=child.is_file(),
        )
        childrenStructures.append(childStructure)
        
        if child.is_file():
            childPath = getFilePathString(child)
            childPieceIndices = filePathsVsPieceIndices[childPath]
            if childPieceIndices is None:
                raise KeyError('Unable to find piece indices for file - {}'.format(childPath))
            childStructure.setPieceIndicesRange(childPieceIndices)
        
        if child.is_dir():
            grandchildrenStructures = getDirectoryStructure(child, filePathsVsPieceIndices)
            childStructure.setChildrenStructures(grandchildrenStructures)
    
    return tuple(childrenStructures)


def populateDirectoryPieceDetails(metadata: Metadata):
    descendantPaths = getSortedDescendantFilePathStrings(metadata.transferPath)
    descendantVsPieceIndices = populateDirectoryPieceHashes(metadata, descendantPaths)
    metadata.structure.setChildrenStructures(getDirectoryStructure(metadata.transferPath, descendantVsPieceIndices))


def populateFilePieceDetails(metadata: Metadata):
    metadata.structure.setPieceIndicesRange(PieceIndicesRange(
        start=getPieceIndexValue(0),
        end=getPieceIndexValue(metadata.numberOfPieces - 1, metadata.pieceSize - 1)
    ))
    
    with metadata.transferPath.open('rb') as file:
        pieceHashes = list()
        
        for pieceIndex in range(metadata.numberOfPieces):
            piece = file.read(metadata.pieceSize)
            if len(piece) > 0:
                pieceHashes.append(getPieceHash(piece))
                continue
            break
        
        metadata.setPieceHashes(tuple(pieceHashes))
