from collections import defaultdict
from queue import Queue
import bisect

from typing import List


class FileSystem:
    MAX_DIR_ELEMENTS: int
    MAX_BUF_FILE_SIZE: int

    def __init__(self, max_elems: int, max_buf_file_size: int):
        self.MAX_DIR_ELEMENTS = max_elems
        self.MAX_BUF_FILE_SIZE = max_buf_file_size

        self.paths = defaultdict(list)
        self.binfiles = defaultdict(str)
        self.logfiles = defaultdict(str)
        self.buffiles = defaultdict(Queue)

    def mkdir(self, path: str) -> bool:
        if path in self.paths:
            print("Directory is already exists")
            return False
        if ".bin" in path or ".log" in path or ".buf" in path:
            print("Incorrect path")
            return False
        if self.check_ancestor_dir(path):
            self.paths[path]
            return True
        else:
            return False

    def ls(self, path: str) -> List[str]:
        if path.endswith(".bin") or path.endswith(".log") or path.endswith(".buf"):
            return [path.split("/")[-1]]
        else:
            return self.paths[path]

    def check_ancestor_dir(self, path: str) -> bool:
        if ".bin" in path or ".log" in path or ".buf" in path:
            print("Incorrect path")
            return False
        directories = path.split("/")

        for i in range(1, len(directories)):
            cur = "/".join(directories[:i]) or "/"

            if cur not in self.paths or directories[i] not in self.paths[cur]:
                if len(self.paths[cur]) < self.MAX_DIR_ELEMENTS:
                    bisect.insort(self.paths[cur], directories[i])
                else:
                    print("Directory is full")
                    return False
        return True

    def move_directory(self, path: str, pathTo: str) -> bool:
        if path in self.paths:
            dirs = path.split("/")
            name = dirs[len(dirs) - 1]

            if name not in self.paths[pathTo]:
                if len(self.paths[pathTo]) < self.MAX_DIR_ELEMENTS:
                    self.delete_directory(path)
                    path_to_name = pathTo + "/" + name
                    self.mkdir(path_to_name)
                    return True
                else:
                    print("Directory is already full")
                    return False
            else:
                print("Directory with such name is already exists")
                return False
        else:
            print("Directory doesn't exist")
            return False

    def delete_directory(self, path: str) -> bool:
        if path in self.paths:
            length = self.ls(path)
            if len(length) == 0:
                dirs = path.split("/")
                parent_dir = "/".join(dirs[:-1])

                self.paths[parent_dir].remove(dirs[len(dirs) - 1])
                self.paths.pop(path)
                return True
            else:
                print("Cannot delete non-empty directory")
                return False
        else:
            print("There is no such directory")
            return False

    def create_binary_file(self, path: str, fileName: str, content: str = 'Lab1') -> bool:
        if fileName.endswith(".bin"):
            if path != "/":
                if self.check_ancestor_dir(path):
                    if fileName not in self.paths[path]:
                        if len(self.paths[path]) < self.MAX_DIR_ELEMENTS:
                            file_path = path + "/" + fileName
                            bisect.insort(self.paths[path], fileName)
                            self.binfiles[file_path] = content
                            return True
                        else:
                            print("Directory is already full")
                            return False
                    else:
                        print("File is already exists")
                        return False
                else:
                    return False
            else:
                print("You should create a directory firstly")
                return False
        else:
            print("You've entered the Incorrect file name")
            return False

    def delete_binary_file(self, file_path: str) -> bool:
        if file_path in self.binfiles:
            directories = file_path.split("/")

            dir_path = "/".join(directories[:-1])
            self.paths[dir_path].remove(directories[len(directories) - 1])
            self.binfiles.pop(file_path)
            return True
        else:
            print("File doesn't exist")
            return False

    def read_binary_file(self, file_path: str) -> str:
        if file_path in self.binfiles:
            return self.binfiles[file_path]
        else:
            print("File doesn't exist")
            return None

    def move_binary_file(self, file_path: str, pathTo: str) -> bool:
        if file_path in self.binfiles:
            dirs = file_path.split("/")
            file_name = dirs[len(dirs) - 1]

            if file_name not in self.paths[pathTo]:
                if len(self.paths[pathTo]) < self.MAX_DIR_ELEMENTS:
                    self.delete_binary_file(file_path)
                    self.create_binary_file(pathTo, file_name)
                    return True
                else:
                    print("Directory is already full")
                    return False
            else:
                print("File with such name already exists")
                return False
        else:
            print("File doesn't exist")
            return False

    def create_log_file(self, path: str, fileName: str) -> bool:
        if fileName.endswith(".log"):
            if path != "/":
                if self.check_ancestor_dir(path):
                    if fileName not in self.paths[path]:
                        if len(self.paths[path]) < self.MAX_DIR_ELEMENTS:
                            file_path = path + "/" + fileName
                            bisect.insort(self.paths[path], fileName)
                            self.logfiles[file_path] = ""
                            return True
                        else:
                            print("Directory is already full")
                            return False
                    else:
                        print("File is already exists")
                        return False
                else:
                    return False
            else:
                print("You should create a directory firstly")
                return False
        else:
            print("You've entered the Incorrect file name")
            return False

    def delete_log_file(self, file_path: str) -> bool:
        if file_path in self.logfiles:
            directories = file_path.split("/")
            dir_path = "/".join(directories[:-1])
            self.paths[dir_path].remove(directories[len(directories) - 1])
            self.logfiles.pop(file_path)
            return True
        else:
            print("File doesn't exist")
            return False

    def append_text(self, file_path: str, text: str) -> bool:
        if file_path not in self.logfiles:
            dirs = file_path.split("/")
            file_name = dirs[len(dirs) - 1]
            dir_path = "/".join(dirs[:-1])
            b = self.create_log_file(dir_path, file_name)
            if not b:
                return False

        if self.logfiles[file_path] != "":
            self.logfiles[file_path] += "\n\r"
        self.logfiles[file_path] += text
        if text in self.logfiles[file_path]:
            return True
        else:
            print("Error: Something went wrong")
            return False

    def read_log_file(self, file_path: str) -> str:
        if file_path in self.logfiles:
            return self.logfiles[file_path]
        else:
            print("File doesn't exist")
            return None

    def move_log_file(self, file_path: str, pathTo: str) -> bool:
        if file_path in self.logfiles:
            dirs = file_path.split("/")
            file_name = dirs[len(dirs) - 1]

            if file_name not in self.logfiles[pathTo]:
                text = self.logfiles[file_path]

                if len(self.paths[pathTo]) < self.MAX_DIR_ELEMENTS:
                    self.delete_log_file(file_path)
                    self.create_log_file(pathTo, file_name)

                    new_file_path = pathTo + "/" + file_name
                    self.append_text(new_file_path, text)
                    return True
                else:
                    return False
            else:
                print("File with such name already exists")
                return False
        else:
            print("File doesn't exist")
            return False

    def create_buf_file(self, path: str, fileName: str) -> bool:
        if fileName.endswith(".buf"):
            if path != "/":
                if self.check_ancestor_dir(path):
                    if fileName not in self.paths[path]:
                        if len(self.paths[path]) < self.MAX_DIR_ELEMENTS:
                            file_path = path + "/" + fileName
                            bisect.insort(self.paths[path], fileName)
                            self.buffiles[file_path] = Queue(maxsize=self.MAX_BUF_FILE_SIZE)
                            return True
                        else:
                            print("Directory is already full")
                            return False
                    else:
                        print("File is already exists")
                        return False
                else:
                    return False
            else:
                print("You should create a directory firstly")
                return False
        else:
            print("You've entered the Incorrect file name")
            return False

    def delete_buf_file(self, file_path: str) -> bool:
        if file_path in self.buffiles:
            directories = file_path.split("/")

            dir_path = "/".join(directories[:-1])
            self.paths[dir_path].remove(directories[len(directories) - 1])
            self.buffiles.pop(file_path)
            return True
        else:
            print("File doesn't exist")
            return False

    def push_to_buf_file(self, file_path: str, elem) -> bool:
        if file_path not in self.buffiles:
            dirs = file_path.split("/")
            file_name = dirs[len(dirs) - 1]
            dir_path = "/".join(dirs[:-1])
            b = self.create_buf_file(dir_path, file_name)
            if not b:
                return False
        if not self.buffiles[file_path].full():
            self.buffiles[file_path].put(elem)
            return True
        else:
            print("Queue is already full")
            return False

    def consume_from_buf_file(self, file_path: str):
        if file_path not in self.buffiles:
            print("File doesn't exist")
            return False
        elif self.buffiles[file_path].empty():
            print("Queue is already empty")
            return False
        else:
            return self.buffiles[file_path].get()

    def move_buf_file(self, file_path: str, pathTo: str) -> bool:
        if file_path in self.buffiles:
            dirs = file_path.split("/")
            file_name = dirs[len(dirs) - 1]

            if file_name not in self.paths[pathTo]:
                if len(self.paths[pathTo]) < self.MAX_DIR_ELEMENTS:
                    self.delete_buf_file(file_path)
                    self.create_buf_file(pathTo, file_name)
                    return True
                else:
                    print("Directory is already full")
                    return False
            else:
                print("File with such name already exists")
                return False
        else:
            print("File doesn't exist")
            return False


fs = FileSystem(5, 5)
fs.mkdir("/life_campus")
fs.mkdir("/life_campus/work")
fs.mkdir("/life_campus/games")

fs.create_binary_file("/life_campus/work", "trash_bin_file.bin", "---LAB_1---")
print(fs.read_binary_file("/life_campus/work/trash_bin_file.bin"))
fs.create_log_file("/life_campus/work", "lab1.log")

fs.append_text("/life_campus/work/lab1.log", "Oleksii\n\rFadeev")
fs.append_text("/life_campus/work/lab1.log", "KP-03 FAM")
fs.append_text("/life_campus/work/lab1.log", "lab show time")

fs.create_buf_file("/life_campus/university", "text.buf")
fs.push_to_buf_file("life_campus/university/text.buf", "First")
fs.push_to_buf_file("life_campus/university/text.buf", "Second")
fs.push_to_buf_file("life_campus/university/text.buf", "Third")
fs.push_to_buf_file("life_campus/university/text.buf", "Fourth")

print()
print(fs.consume_from_buf_file("life_campus/university/text.buf"))
print(fs.consume_from_buf_file("life_campus/university/text.buf"))
print(fs.consume_from_buf_file("life_campus/university/text.buf"))
print(fs.consume_from_buf_file("life_campus/university/text.buf"))

print()

print("Raw text example:\n\r" + fs.read_log_file("/life_campus/work/lab1.log"))

print()

fs.mkdir("/life_campus/no_content")
print(fs.ls("/life_campus"))
fs.delete_directory("/life_campus/no_content")
print(fs.ls("/life_campus"))

fs.mkdir("/life_campus/test_move")
print(fs.ls("/life_campus"))
fs.move_directory("/life_campus/test_move", "/life_campus/work")
print(fs.ls("/life_campus"))
print(fs.ls("/life_campus/work"))

fs.mkdir("/life_campus")
