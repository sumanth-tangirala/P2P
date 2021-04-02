import math
import hashlib


def getPieceDetails(transferSize: int):
    # TODO: Dynamic piece size
    return {
        'pieceSize': 500,
        'numberOfPieces': math.ceil(transferSize / 500),
    }


def getPieceHash(piece: bytes):
    return hashlib.sha3_256(piece).hexdigest()


def getPieceIndexValue(pieceIndex: int, byteIndex: int = 0):
    return '{}.{}'.format(pieceIndex, byteIndex)
