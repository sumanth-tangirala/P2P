class PieceFileByteIndices:
    def __init__(self, fileId: int, fileStartByteIndex: int = None):
        self.fileId = fileId
        self.fileStartByteIndex = fileStartByteIndex
        self.fileEndByteIndex = None
        
    def setFileEndByteIndex(self, fileEndByteIndex: int):
        self.fileEndByteIndex = fileEndByteIndex
    
    def toJSON(self):
        return {
            "fileId": self.fileId,
            "fileStartByteIndex": self.fileStartByteIndex,
            "fileEndByteIndex": self.fileEndByteIndex,
        }
