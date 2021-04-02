from pathlib import Path

from functools import reduce
import bisect


def getChildFilePath(parentPath: str, childName: str):
    return '{}/{}'.format(parentPath, childName)


def getFileSize(path: Path):
    fileStats = path.stat()
    return fileStats.st_size


def getTransferSize(transferPath: Path):
    if transferPath.is_file():
        return getFileSize(transferPath)
    
    if transferPath.is_dir():
        return reduce(lambda totalSize, child: totalSize + getTransferSize(child), transferPath.iterdir(), 0)
    
    return 0


def getFilePathString(path: Path):
    return str(path.absolute())


# Follows DFS and insertion sort
def getSortedDescendantFilePathStrings(parentPath: Path):
    descendantPathList = list()
    directoryChildren = list()
    
    for child in parentPath.iterdir():
        if child.is_dir():
            bisect.insort_right(directoryChildren, child)
        else:
            bisect.insort_right(descendantPathList, getFilePathString(child))
    
    for directoryChild in directoryChildren:
        descendantPathList.extend(getSortedDescendantFilePathStrings(directoryChild))
    return tuple(descendantPathList)
