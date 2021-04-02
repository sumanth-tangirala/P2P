# Classes
from .PieceIndicesRange import PieceIndicesRange


class Structure:
    def __init__(self, name: str, isFile: bool = True):
        self.name = name
        self.pieceIndicesRange = None
        self.children = None
        self.isFile = isFile
    
    def setPieceIndicesRange(self, pieceIndicesRange: PieceIndicesRange):
        self.pieceIndicesRange = pieceIndicesRange
    
    def setChildrenStructures(self, childrenStructures: tuple):
        self.children = childrenStructures
