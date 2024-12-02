import pytest
from shell import Shell
from filesystem import VirtualFileSystem

@pytest.fixture
def shell():
    vfs = VirtualFileSystem("linux_filesystem.zip")
    return Shell("test_user", "test_host", vfs)


def test_ls(shell):
    result = shell.execute("ls")
    assert result == "bin\netc\nhome\nusr\nvar"


def test_cd(shell):
    shell.execute("cd /bin")
    assert shell.vfs.current_path == "~/bin"
    result = shell.execute("ls")
    assert result == "cat\nls"


def test_whoami(shell):
    result = shell.execute("whoami")
    assert result == "test_user"


def test_exit(shell):
    shell.execute("exit")
    assert not shell.running


def test_find(shell):
    result = shell.execute("find home")
    assert result == "~/home"


def test_wc(shell):
    shell.execute("cd /home/user")
    result = shell.execute("wc file1.txt")
    assert result == "1 5 28"


def test_unknown_command(shell):
    result = shell.execute("unknown_command")
    assert result == "Неизвестная команда: unknown_command"
