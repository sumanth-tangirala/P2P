from pathlib import Path

# PyDash
from pydash.objects import get
from pydash.collections import reduce_

# Classes
from Classes.Metadata.Metadata import Metadata

# Helpers
from Classes.Downloader.DownloaderHelpers import generateShellFileStructure, populateFilesFromPiece, updateFileIdVsFilePathWithNewTargetName
from helpers.piece import getPieceHash

# TODO: Make Downloader use the same bitmap as Seeder
# TODO: Check if temp dir mode is necessary
class Downloader:
    def __init__(self, metadata: Metadata, downloadDirectoryPath: Path, pieceBitMap: list, fileIdVsFilePath: dict):
        piecesDirectoryPath = downloadDirectoryPath.joinpath('.{}.temp.download'.format(metadata.name))
        piecesDirectoryPath.mkdir(parents=True, exist_ok=True)
        
        self._metadata = metadata
        self._pieceBitMap = pieceBitMap
        self._downloadDirectoryPath = downloadDirectoryPath
        self._fileIdVsFilePath = fileIdVsFilePath
        self._piecesDirectoryPath = piecesDirectoryPath
        self._erroredFiles = set()
        self._numberOfPiecesToDownload = reduce_(pieceBitMap, lambda acc, isPieceDownloaded: acc if isPieceDownloaded else acc + 1, 0)
        
    def _storePiece(self, piece, pieceIndex):
        piecePath = self._piecesDirectoryPath.joinpath(str(pieceIndex))
        with piecePath.open(mode="wb") as pieceFile:
            pieceFile.write(piece)
        self._pieceBitMap[pieceIndex] = True
        self._numberOfPiecesToDownload -= 1
        
        
    def _constructFilesFromPieces(self):
        newDownloadTargetName = generateShellFileStructure(self._metadata.structure, self._downloadDirectoryPath)
        self._fileIdVsFilePath = updateFileIdVsFilePathWithNewTargetName(self._fileIdVsFilePath, newDownloadTargetName)
        
        for pieceIndex in range(self._metadata.numberOfPieces):
            pieceFilePath = self._piecesDirectoryPath.joinpath(str(pieceIndex))
            erroredFiles = populateFilesFromPiece(
                pieceFilePath=pieceFilePath,
                pieceDetails=self._metadata.pieceDetailsList[pieceIndex],
                fileIdVsFilePath=self._fileIdVsFilePath,
                downloadDirectoryPath=self._downloadDirectoryPath,
            )
            self._erroredFiles.update(erroredFiles)
            if pieceFilePath.exists():
                pieceFilePath.unlink()
        
        self._piecesDirectoryPath.rmdir()
        
                    
    
    def downloadPiece(self, receivedPiece: bytes, index: int):
        receivedPieceHash = getPieceHash(receivedPiece)
        expectedPieceHash = get(self._metadata, ['pieceDetailsList', index, 'pieceHash'])
        
        if receivedPieceHash != expectedPieceHash:
            raise ValueError('Hash mismatch')
        
        self._storePiece(receivedPiece, index)
        if self._numberOfPiecesToDownload == 0:
            self._constructFilesFromPieces()
