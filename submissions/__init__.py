"""Submissions"""
import os
import os.path
import re
from pathlib import Path
from subprocess import check_output
from typing import Any, Callable, Union

__version__ = "2022.1"
handle_pattern = re.compile(r"[a-z]{2}[0-9]{6}")
archive_suffixes = [".zip", ".tar", ".tar.gz", ".7z"]


class Submissions:
    """Abstraction of the submisison direcotyr root."""

    def __init__(self, root: Union[Path, str]):
        if isinstance(root, str):
            root = Path(root)
        self.root = root

    def list(self) -> list[Path]:
        """List of path that match student email handle."""
        items = [i for i in self.root.iterdir() if i.is_dir()]
        handles = [i for i in items if is_student_folder(i) is not None]
        return handles

    def run_shell_command(self, shell_cmd: str) -> list[Any]:
        """For each submission, run a shell command."""
        pass

    def map(self, op: Callable[Path, Any]) -> list[Any]:
        """For each submission, call the Callable of type Path -> Any."""
        return [op(p) for p in self.list()]


def is_student_folder(path: Path) -> bool:
    """
    True if path is the student folder. False otherwise.

    The path is a sub directory in the student folder, result will
    be False.
    """
    return handle_pattern.match(path.name) is not None


def get_all_files(root: Path) -> list:
    """List all files in the folder and sub-folders."""
    if not root.is_dir():
        return []

    all_files = []
    for path, subdirs, files in os.walk(str(root)):
        print(path, files)
        p = Path(path)

        # Ignoring any result within __MAXOSX.
        # It can contains file with suffix like .tar.gz, .zip
        # but these file are not actually the archive file.
        if "__MACOSX" in p.parts or ".git" in p.parts or ".github" in p.parts:
            continue

        for f in files:
            all_files.append(p / f)
    return all_files


def is_archive_file(suffix: str) -> bool:
    """True if the suffix is of an archive file. False otherwise."""
    return (
        suffix == ".zip" or suffix == ".tar" or suffix == ".tar.gz" or suffix == ".7z"
    )


def get_archive_files(root: Path) -> list:
    """List only archive files in the directory and sub-directoies."""
    files = get_all_files(root)
    return [f for f in files if is_archive_file("".join(f.suffixes))]


def find_makefiles(path: Path) -> list[Path]:
    """
    Return list of Makefile found within the path.

    This searches sub-folders and nested archive files.
    Side effect of this fucntion includes extracted files
    being left on disk.
    """
    if not path.is_dir():
        return []

    found_makefiles = []
    paths = [path]

    while len(paths) != 0:
        print("\n\n\n --- New Iteration", paths)
        path = paths.pop()

        # get list of all files.
        all_files = get_all_files(path)

        for f in all_files:
            print(f)
            if f.name == "makefile" or f.name == "Makefile":
                found_makefiles.append(f)

        archive_files = [f for f in all_files if is_archive_file("".join(f.suffixes))]
        if len(archive_files) == 0:
            continue

        # make a directory next to the file.
        for af in archive_files:
            # skip empty archive.
            if os.path.getsize(str(af)) == 0:
                continue

            dir_name = f"{af.stem}__extracted"
            try:
                dir_path = af.parent / dir_name
                os.mkdir(str(dir_path))

                suffix = "".join(af.suffixes)
                if suffix == ".zip":
                    # extract a zip file.
                    _ = check_output(["unzip", str(af), "-d", str(dir_path)])
                elif suffix == ".tar.gz":
                    _ = check_output(["tar", "-xzf", str(af), "-C", str(dir_path)])
                elif suffix == ".7z":
                    _ = check_output(
                        ["7z", "e", "-y", str(af), f"-o{str(dir_path)}", "*"]
                    )

                paths.append(dir_path)
            except FileExistsError:
                pass

    return found_makefiles


if __name__ == "__main__":
    pass
