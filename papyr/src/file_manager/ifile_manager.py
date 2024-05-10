from abc import ABC, abstractmethod


class IFileManager(ABC):
    @abstractmethod
    def upload_file(self, source, destination):
        pass

    @abstractmethod
    def download_file(self, source, destination):
        pass

    @abstractmethod
    def delete_file(self, file_path):
        pass

    @abstractmethod
    def list_files(self, prefix):
        pass
