from collections import defaultdict
from queue import Queue
import bisect

class FileSystem:
    
    DIR_MAX_ELEMS: int
    MAX_BUF_FILE_SIZE: int

    def __init__(self, max_elems: int, max_buf_file_size: int):
        pass
    
    def ls(self, path: str) -> list[str]: 
        pass

    def mkdir(self, path: str) -> bool:
        pass

    def check_ancestor_dir(self, path: str) -> bool:
        pass
    
    def delete_directory(self, path: str) -> bool:
        pass

    def move_directory(self, path: str, pathTo: str) -> bool:
        pass

    def create_binary_file(self, path: str, fileName: str) -> bool:
        pass

    def delete_binary_file(self, filePath: str) -> bool:
        pass

    def read_binary_file(self, filePath: str) -> str:
        pass
        

    def move_binary_file(self, filePath: str, pathTo: str) -> bool:
        pass


    def create_log_file(self, path: str, fileName: str) -> bool:
        pass

    def delete_log_file(self, filePath: str) -> bool:
        pass

    def append_text(self, filePath: str, text: str) -> bool:
        pass

    def read_log_file(self, filePath: str) -> str:
        pass

    def move_log_file(self, filePath: str, pathTo: str) -> bool:
        pass
    
    def create_buf_file(self, path: str, fileName: str) -> bool:
        pass

    def delete_buf_file(self, filePath: str) -> bool:
        pass

    def push_to_buf_file(self, filePath: str, elem) -> bool:
        pass

    def consume_from_buf_file(self, filePath: str):
        pass
    
    def move_buf_file(self, filePath: str, pathTo: str) -> bool:
        pass
