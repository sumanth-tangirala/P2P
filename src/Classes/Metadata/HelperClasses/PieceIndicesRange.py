class PieceIndicesRange:
    def __init__(self, start: str = None, end: str = None):
        self.start = start
        self.end = end
    
    def setStart(self, start: str):
        self.start = start
    
    def setEnd(self, end: str):
        self.end = end
    
    def __repr__(self):
        # TODO: Remove
        return '{{ start: {0}, end: {1}}}'.format(self.start, self.end)
    
    def __str__(self):
        return '{{ start: {0}, end: {1}}}'.format(self.start, self.end)
