class PieceDetails:
    def __init__(self, pieceHash: str, pieceFileByteIndicesList: tuple):
        self.pieceHash = pieceHash
        self.pieceFileByteIndicesList = pieceFileByteIndicesList
        
    def toJSON(self):
        return {
            "pieceHash": self.pieceHash,
            "pieceFileByteIndicesList": list(map(lambda pieceFileIndices: pieceFileIndices.toJSON(), self.pieceFileByteIndicesList)),
        }
