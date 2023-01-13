from file_system import FileSystem
import pytest


@pytest.fixture
def file_system():
    fs = FileSystem(5, 5)
    fs.mkdir("/mainFolder")
    return fs


@pytest.fixture
def file_system_with_files():
    fs = FileSystem(5, 5)
    fs.mkdir("/mainFolder1")
    fs.mkdir("/mainFolder1/mainFolder1-1")
    fs.mkdir("/mainFolder1/mainFolder1-2")

    fs.create_binary_file("/mainFolder1/mainFolder1-1", "bin_file.bin")
    fs.create_log_file("/mainFolder1/mainFolder1-1", "logfile.log")
    fs.create_buf_file("/mainFolder1/mainFolder1-2", "buf_file.buf")
    fs.create_log_file("/mainFolder1/mainFolder1-2", "logfile.log")
    return fs


@pytest.fixture
def file_system_dir_overflow():
    fs = FileSystem(5, 5)
    fs.mkdir("/mainFolder1")
    fs.create_binary_file("/mainFolder1", "1.bin")
    fs.create_binary_file("/mainFolder1", "2.bin")
    fs.create_binary_file("/mainFolder1", "3.bin")
    fs.create_binary_file("/mainFolder1", "4.bin")
    fs.create_binary_file("/mainFolder1", "5.bin")
    return fs


# -------------------------------------------------------------------------------------
def test_ls_1(file_system_with_files):
    assert file_system_with_files.ls("/mainFolder1/mainFolder1-1") == ['bin_file.bin', 'logfile.log']


def test_ls_2(file_system_with_files):
    assert file_system_with_files.ls("/mainFolder1/mainFolder1-2") == ['buf_file.buf', 'logfile.log']


def test_ls_3(file_system_with_files):
    assert file_system_with_files.ls("/") == ['mainFolder1']


# -------------------------------------------------------------------------------------

def test_mkdir_simple_good(file_system):
    file_system.mkdir("/mainFolder")
    assert file_system.ls("/") == ['mainFolder']


def test_mkdir_nested_good(file_system_with_files):
    file_system_with_files.mkdir("/mainFolder1/mainFolder1-3")
    assert file_system_with_files.ls("/mainFolder1") == ['mainFolder1-1', 'mainFolder1-2', 'mainFolder1-3']


def test_mkdir_some_dirs_missing(file_system):
    file_system.mkdir("/mainFolder1/mainFolder2")
    assert file_system.ls("/mainFolder1") == ['mainFolder2']


def test_mkdir_overflow_bad(file_system_dir_overflow):
    assert file_system_dir_overflow.mkdir("/mainFolder1/mainFolder2") is False


def test_mkdir_incorrect_path_bad(file_system):
    assert file_system.mkdir("/bad_folder.log") is False

# ---------------------------------------------------------------------------------------
