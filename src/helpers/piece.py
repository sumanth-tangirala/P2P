import math
from pathlib import Path
import hashlib
import os

# Classes
from Classes.Metadata.HelperClasses.PieceFileByteIndices import PieceFileByteIndices

def getPieceDetails(transferSize: int):
    # TODO: Dynamic piece size
    pieceSize = 500
    numberOfPieces = math.ceil(transferSize / pieceSize)
    return pieceSize, numberOfPieces


def getPieceHash(piece: bytes):
    return hashlib.sha3_256(piece).hexdigest()


def getPieceGenerator(filePaths: tuple, descendantFilePathsVsId: dict, pieceSize: int, numberOfPieces: int):
    currentDescendantIndex = 0
    currentDescendantPath = filePaths[currentDescendantIndex]
    currentDescendantFile = open(currentDescendantPath, 'rb')
    cursorBytePosition = 0
    
    def updateToNextCurrentDescendant(pieceFileByteIndicesList: list):
        nonlocal currentDescendantIndex
        nonlocal currentDescendantFile
        nonlocal cursorBytePosition

        pieceFileByteIndicesList[-1].setFileEndByteIndex(cursorBytePosition)
        
        if currentDescendantFile is not None:
            currentDescendantFile.close()
        
        currentDescendantIndex += 1
        nextDescendantPath = filePaths[currentDescendantIndex]
        currentDescendantFile = open(nextDescendantPath, 'rb')
        cursorBytePosition = 0
        pieceFileByteIndicesList.append(PieceFileByteIndices(
            fileId=descendantFilePathsVsId[filePaths[currentDescendantIndex]],
            fileStartByteIndex=cursorBytePosition
        ))
    
    for pieceIndex in range(numberOfPieces):
        piece = currentDescendantFile.read(pieceSize)
        pieceFileByteIndicesList = [PieceFileByteIndices(
            fileId=descendantFilePathsVsId[filePaths[currentDescendantIndex]],
            fileStartByteIndex=cursorBytePosition,
        )]
        cursorBytePosition += len(piece)
        
        while len(piece) < pieceSize and currentDescendantIndex < len(filePaths) - 1:
            updateToNextCurrentDescendant(pieceFileByteIndicesList)
            nextPieceData = currentDescendantFile.read(pieceSize - len(piece))
            cursorBytePosition += len(nextPieceData)
            piece = piece + nextPieceData

        if len(piece) == 0:
            break
        pieceFileByteIndicesList[-1].setFileEndByteIndex(cursorBytePosition)
        yield piece, tuple(pieceFileByteIndicesList)

    currentDescendantFile.close()

def getPieceFromFileByteIndices(pieceFileByteIndicesList: tuple, sourcePath: Path, fileIdVsFilePath: dict):
    piece = b''
    for pieceFileByteIndices in pieceFileByteIndicesList:
        try:
            filePath = '{}/{}'.format(str(sourcePath.absolute()), fileIdVsFilePath[pieceFileByteIndices.fileId])
            with open(filePath, 'rb') as file:
                startIndex = 0
                endIndex = os.path.getsize(filePath)
                if pieceFileByteIndices.fileStartByteIndex is not None: # TODO: Handle after metadata json-ing
                    startIndex = pieceFileByteIndices.fileStartByteIndex
                    file.seek(startIndex)
                if pieceFileByteIndices.fileEndByteIndex is not None: # TODO: Handle after metadata json-ing
                    endIndex = pieceFileByteIndices.fileEndByteIndex
                sizeToRead = endIndex - startIndex
                piece += file.read(sizeToRead)
        except FileNotFoundError:
            continue # TODO: Handle by directly stopping piece generation
    return piece
