from abc import ABC, abstractmethod
from io import BytesIO


class IFileManager(ABC):
    @abstractmethod
    def upload_file(self, file: BytesIO, path: str) -> bool:
        pass

    @abstractmethod
    def download_file(self, path: str) -> BytesIO:
        pass

    @abstractmethod
    def delete_file(self, path: str) -> bool:
        pass

    @abstractmethod
    def list_files(self, prefix):
        pass
