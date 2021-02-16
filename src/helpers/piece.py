import math
import hashlib

def getPieceDetails(transferSize: int):
	return [500, math.ceil(transferSize/500)]

def getPieceHash(piece):
	return hashlib.sha3_256(piece).hexdigest()
