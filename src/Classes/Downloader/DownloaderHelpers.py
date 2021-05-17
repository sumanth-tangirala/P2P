from pathlib import Path

# Classes
from Classes.Metadata.HelperClasses.PieceDetails import PieceDetails
from Classes.Metadata.HelperClasses.Structure import Structure

def generateShellFileStructure(structure: Structure, parentDirectoryPath: Path, isChildStructure: bool = False):
    currentPath = parentDirectoryPath.joinpath(structure.name)
    nameStem = currentPath.stem
    nameSuffix = currentPath.suffix
    downloadNumber = 1
    while not isChildStructure and currentPath.exists():
        newFileOrDirName = '{}({}){}'.format(nameStem, downloadNumber, nameSuffix)
        currentPath = parentDirectoryPath.joinpath(newFileOrDirName)
        downloadNumber += 1
    if structure.isFile:
        currentPath.touch()
    else:
        currentPath.mkdir()
        for child in structure.children:
            generateShellFileStructure(child, currentPath, True)
    return currentPath.name

def populateFilesFromPiece(pieceFilePath: Path, pieceDetails: PieceDetails, fileIdVsFilePath: dict, downloadDirectoryPath: Path):
    erroredFiles = list()
    
    with pieceFilePath.open('rb') as pieceFile:
        for pieceFileByteIndices in pieceDetails.pieceFileByteIndicesList:
            relativeFilePath = fileIdVsFilePath[pieceFileByteIndices.fileId]
            filePath = downloadDirectoryPath.joinpath(relativeFilePath)
            numberOfBytesToTransfer = pieceFileByteIndices.fileEndByteIndex - pieceFileByteIndices.fileStartByteIndex
            try:
                with filePath.open('ab') as downloadFile:
                    dataToTransfer = pieceFile.read(numberOfBytesToTransfer)
                    downloadFile.write(dataToTransfer)
            except:
                erroredFiles.append(relativeFilePath)
    
    return set(erroredFiles)

def updateFileIdVsFilePathWithNewTargetName(fileIdVsFilePath: dict, newTargetName: str):
    updatedFileIdVsFilePath = dict()
    for fileId in fileIdVsFilePath:
        prevFilePath = fileIdVsFilePath[fileId]
        pathParts = prevFilePath.split('/')
        pathParts[0] = newTargetName
        updatedFileIdVsFilePath[fileId] = '/'.join(pathParts)
    return updatedFileIdVsFilePath
