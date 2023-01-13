from file_system import FileSystem
import pytest


@pytest.fixture
def file_system():
    fs = FileSystem(5, 5)
    fs.mkdir("/main")
    return fs


@pytest.fixture
def file_system_with_files():
    fs = FileSystem(5, 5)
    fs.mkdir("/mainFolder")
    fs.mkdir("/mainFolder/mainFolder-1")
    fs.mkdir("/mainFolder/mainFolder-2")
    fs.mkdir("/mainFolder/mainFolder-3")

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


# --------------------------------------------------------------

def test_create_log_file_simple_good(file_system):
    file_system.create_log_file("/main", "logfile.log")
    assert file_system.ls("/main") == ['logfile.log']


def test_create_log_file_dirs_missing_good(file_system):
    file_system.create_log_file("/main/mainFolder/main2", "logfile.log")
    assert file_system.ls("/main/mainFolder/main2") == ['logfile.log']


def test_create_log_file_no_directory_bad():
    fs = FileSystem(5, 5)
    assert fs.create_log_file("/", "logfile.log") is False


def test_create_log_file_incorrect_extension_bad(file_system):
    assert file_system.create_log_file("/main", "some.lo") is False


def test_create_log_file_dir_is_full_bad(file_system_dir_overflow):
    assert file_system_dir_overflow.create_log_file("/mainFolder", "some.log") is False


def test_create_log_file_already_exists_bad(file_system_with_files):
    assert file_system_with_files.create_log_file("/mainFolder/mainFolder-1", "logfile.log") is False


def test_create_log_file_impossible_path(file_system):
    assert file_system.create_log_file("/main/main.log", "some.log") is False


# ---------------------------------------------------------------------------------------------

def test_delete_log_file_simple_good(file_system_with_files):
    file_system_with_files.delete_log_file("/mainFolder/mainFolder-1/logfile.log")
    assert file_system_with_files.ls("/mainFolder/mainFolder-1") == ['bin_file.bin']


def test_delete_log_file_doesnt_exist(file_system):
    assert file_system.delete_log_file("/main/log.log") is False


# ---------------------------------------------------------------------------------------------

def test_read_log_file_and_append_text_simple_good(file_system_with_files):
    file_system_with_files.append_text("/mainFolder/mainFolder-1/logfile.log", "some text")
    assert file_system_with_files.read_log_file("/mainFolder/mainFolder-1/logfile.log") == "some text"


def test_read_log_file_doesnt_exist_bad(file_system):
    assert file_system.read_log_file("/main/log.log") is None


def test_read_log_file_several_lines_good(file_system_with_files):
    file_system_with_files.append_text("/mainFolder/mainFolder-1/logfile.log", "some text")
    file_system_with_files.append_text("/mainFolder/mainFolder-1/logfile.log", "another text")
    assert file_system_with_files.read_log_file("/mainFolder/mainFolder-1/logfile.log") == "some text\n\ranother text"


# ---------------------------------------------------------------------------------------------

def test_append_text_several_lines(file_system_with_files):
    file_system_with_files.append_text("/mainFolder/mainFolder-1/logfile.log", "some text\n\ranother text\n\rsome "
                                                                               "more text here")
    assert file_system_with_files.read_log_file(
        "/mainFolder/mainFolder-1/logfile.log") == "some text\n\ranother text\n\rsome more text here"


def test_append_text_file_doesnt_exist_good(file_system):
    file_system.append_text("/main/log.log", "some text")
    assert file_system.read_log_file("/main/log.log") == "some text"


# ---------------------------------------------------------------------------------------------

def test_move_log_file_simple_good_1(file_system_with_files):
    file_system_with_files.move_log_file("/mainFolder/mainFolder-1/logfile.log", "/mainFolder/mainFolder-3")
    assert file_system_with_files.ls("/mainFolder/mainFolder-1") == ['bin_file.bin']


def test_move_log_file_simple_good_2(file_system_with_files):
    file_system_with_files.move_log_file("/mainFolder/mainFolder-1/logfile.log", "/mainFolder/mainFolder-3")
    assert file_system_with_files.ls("/mainFolder/mainFolder-3") == ['logfile.log']


def test_move_binary_file_doesnt_exist(file_system_with_files):
    assert file_system_with_files.move_binary_file("/mainFolder/mainFolder-2/bin_file.bin",
                                                   "/mainFolder/mainFolder-1") is False


def test_move_binary_file_overflow(file_system_dir_overflow):
    file_system_dir_overflow.create_binary_file("/main2", "bin_file.bin")
    assert file_system_dir_overflow.move_binary_file("/main2/bin_file.bin",
                                                     "/mainFolder") is False


def test_move_binary_file_such_name_already_exists(file_system_with_files):
    file_system_with_files.create_binary_file("/mainFolder/mainFolder-2", "bin_file.bin")
    assert file_system_with_files.move_binary_file("/mainFolder/mainFolder-1/bin_file.bin",
                                                   "/mainFolder/mainFolder-2") is False
