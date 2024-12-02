import argparse
from shell import Shell
from filesystem import VirtualFileSystem
from gui import ShellGUI


def parse_args():
    parser = argparse.ArgumentParser(description="Shell Emulator")
    parser.add_argument("--user", required=True, help="User name for shell prompt")
    parser.add_argument("--host", required=True, help="Host name for shell prompt")
    parser.add_argument("--fs", required=True, help="Path to virtual filesystem (zip)")
    parser.add_argument("--script", required=False, help="Path to startup script")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    vfs = VirtualFileSystem(args.fs)
    shell = Shell(args.user, args.host, vfs)

    if args.script:
        with open(args.script) as script:
            for line in script:
                shell.execute(line.strip())

    gui = ShellGUI(shell)
    gui.run()
