from pathlib import Path

from pydash.collections import reduce_
import bisect

def getTransferSize(transferPath: Path):
    if transferPath.is_dir():
        return reduce_(transferPath.iterdir(), lambda totalSize, child: totalSize + getTransferSize(child), 0)
    else:
        return transferPath.stat().st_size

# Follows DFS and insertion sort
def getSortedDescendantFilePathStrings(parentPath: Path):
    descendantPathList = list()
    directoryChildren = list()
    
    pathsToCheck = [parentPath] if parentPath.is_file() else parentPath.iterdir()
    
    for child in pathsToCheck:
        if child.is_dir():
            bisect.insort_right(directoryChildren, child)
        else:
            bisect.insort_right(descendantPathList, str(child.absolute()))
    
    for directoryChild in directoryChildren:
        descendantPathList.extend(getSortedDescendantFilePathStrings(directoryChild))
    return tuple(descendantPathList)

# TODO: Make a better id function
def getFilePathToFileIdMapping(filePaths: tuple):
    filePathToFileIdMapping = dict()
    for fileIndex in range(len(filePaths)):
        filePath = filePaths[fileIndex]
        filePathToFileIdMapping[filePath] = fileIndex
    return filePathToFileIdMapping
