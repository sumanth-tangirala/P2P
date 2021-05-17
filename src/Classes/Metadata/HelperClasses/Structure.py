from constants.appConstants import EMPTY_TUPLE


class Structure:
    def __init__(self, name: str, isFile: bool = True, fileId: int = None, childrenStructures: tuple = EMPTY_TUPLE):
        self.name = name
        self.isFile = isFile
        self.fileId = fileId
        self.children = childrenStructures
        
    def toJSON(self):
        if self.isFile:
            return {
                "name": self.name,
                "isFile": self.isFile,
                "fileId": self.fileId,
            }
        else:
            return {
                "name": self.name,
                "isFile": self.isFile,
                "children": list(map(lambda child: child.toJSON(), self.children)),
            }
