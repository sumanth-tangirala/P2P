from pathlib import Path

# Helpers
from helpers.piece import getPieceHash, getPieceFromFileByteIndices


def getInitialPieceBitmap(metadata, sourcePath: Path, fileIdVsFilePath: dict):
    pieceBitmap = list()
    for pieceIndex in range(metadata.numberOfPieces):
        pieceDetails = metadata.pieceDetailsList[pieceIndex]
        try:
            localPiece = getPieceFromFileByteIndices(pieceDetails.pieceFileByteIndicesList, sourcePath, fileIdVsFilePath)
            pieceBitmap.append(getPieceHash(localPiece) == pieceDetails.pieceHash)
        except Exception:
            pieceBitmap.append(False)
    return tuple(pieceBitmap)


