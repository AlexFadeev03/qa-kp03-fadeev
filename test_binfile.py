from file_system import FileSystem
import pytest


@pytest.fixture
def file_system():
    fs = FileSystem(5, 5)
    fs.mkdir("/folder")
    return fs


@pytest.fixture
def file_system_with_files():
    fs = FileSystem(5, 5)
    fs.mkdir("/mainFolder")
    fs.mkdir("/mainFolder/mainFolder-1")
    fs.mkdir("/mainFolder/mainFolder-2")

    fs.create_binary_file("/mainFolder/mainFolder-1", "bin_file.bin")
    fs.create_log_file("/mainFolder/mainFolder-1", "logfile.log")
    fs.create_buf_file("/mainFolder/mainFolder-2", "buf_file.buf")
    fs.create_log_file("/mainFolder/mainFolder-2", "logfile.log")
    return fs


@pytest.fixture
def file_system_dir_overflow():
    fs = FileSystem(5, 5)
    fs.mkdir("/mainFolder")
    fs.create_binary_file("/mainFolder", "1.bin")
    fs.create_binary_file("/mainFolder", "2.bin")
    fs.create_binary_file("/mainFolder", "3.bin")
    fs.create_binary_file("/mainFolder", "4.bin")
    fs.create_binary_file("/mainFolder", "5.bin")
    return fs


# -------------------------------------------------------------------

def test_create_binary_file_simple_good(file_system):
    file_system.create_binary_file("/folder", "bin_file.bin")
    assert file_system.ls("/folder") == ['bin_file.bin']


def test_create_binary_file_dirs_missing_good(file_system):
    file_system.create_binary_file("/folder/mainFolder/folder2", "bin_file.bin")
    assert file_system.ls("/folder/mainFolder/folder2") == ['bin_file.bin']


def test_create_binary_file_no_directory_bad():
    fs = FileSystem(5, 5)
    assert fs.create_binary_file("/", "bin_file.bin") is False


def test_create_binary_file_incorrect_extension_bad(file_system):
    assert file_system.create_binary_file("/folder", "some.bi") is False


def test_create_binary_file_dir_is_full_bad(file_system_dir_overflow):
    assert file_system_dir_overflow.create_binary_file("/mainFolder", "some.bin") is False


def test_create_binary_file_already_exists_bad(file_system_with_files):
    assert file_system_with_files.create_binary_file("/mainFolder/mainFolder-1", "bin_file.bin") is False


def test_create_binary_file_impossible_path(file_system):
    assert file_system.create_binary_file("/folder/folder.bin", "some.bin") is False


# -----------------------------------------------------------------------------------------------

def test_delete_binary_file_simple_good(file_system_with_files):
    file_system_with_files.delete_binary_file("/mainFolder/mainFolder-1/bin_file.bin")
    assert file_system_with_files.ls("/mainFolder/mainFolder-1") == ['logfile.log']


def test_delete_binary_file_doesnt_exist(file_system):
    assert file_system.delete_binary_file("/folder/bin.bin") is False


# -----------------------------------------------------------------------------------------------

def test_read_binary_file_simple_good(file_system_with_files):
    assert file_system_with_files.read_binary_file("/mainFolder/mainFolder-1/bin_file.bin") == "Lab1"


def test_read_binary_file_doesnt_exist_bad(file_system):
    assert file_system.read_binary_file("/folder/bin.bin") is None


# -----------------------------------------------------------------------------------------------

def test_move_binary_file_simple_good_1(file_system_with_files):
    file_system_with_files.move_binary_file("/mainFolder/mainFolder-1/bin_file.bin", "/mainFolder/mainFolder-2")
    assert file_system_with_files.ls("/mainFolder/mainFolder-1") == ['logfile.log']


def test_move_binary_file_simple_good_2(file_system_with_files):
    file_system_with_files.move_binary_file("/mainFolder/mainFolder-1/bin_file.bin", "/mainFolder/mainFolder-2")
    assert file_system_with_files.ls("/mainFolder/mainFolder-2") == ['bin_file.bin', 'buf_file.buf', 'logfile.log']


def test_move_binary_file_doesnt_exist(file_system_with_files):
    assert file_system_with_files.move_binary_file("/mainFolder/mainFolder-2/bin_file.bin", "/mainFolder/mainFolder-1") is False


def test_move_binary_file_overflow(file_system_dir_overflow):
    file_system_dir_overflow.create_binary_file("/folder2", "bin_file.bin")
    assert file_system_dir_overflow.move_binary_file("/folder2/bin_file.bin", "/mainFolder") is False


def test_move_binary_file_such_name_already_exists(file_system_with_files):
    file_system_with_files.create_binary_file("/mainFolder/mainFolder-2", "bin_file.bin")
    assert file_system_with_files.move_binary_file("/mainFolder/mainFolder-1/bin_file.bin", "/mainFolder/mainFolder-2") is False
