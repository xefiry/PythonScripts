import argparse
import os
from enum import StrEnum

import psutil
import userpaths  # type: ignore
from send2trash import send2trash

from utils import get_proc_list, normit
from utils.colors import FG

IGNORE_LIST = ["desktop.ini", "Indexed Locations.search-ms"]


class Type(StrEnum):
    FILE = "File"
    DIRECTORY = "Dir "
    DIRECTORY_FORCED = "Dir+"
    PROCESS = "Proc"


class Result(StrEnum):
    SKIPED = f"{FG.GRAY}Skipped{FG.CLEAR}"
    ERROR = f"{FG.RED}ERROR{FG.CLEAR}"
    OK = f"{FG.WHITE}Ok{FG.CLEAR}"


def is_dir_empty(path: str) -> bool:
    content = os.listdir(path)

    # remove IGNORE_LIST from content
    content = list(set(content) - set(IGNORE_LIST))

    return len(content) == 0


class Item:
    def __init__(self, type: Type, value: str) -> None:
        self.type: Type = type
        self.value: str = value
        self.result: Result = Result.SKIPED
        self.detail: str | None = None

    def process(self) -> None:
        match self.type:
            case Type.FILE:
                self._remove_file()
            case Type.DIRECTORY:
                self._remove_dir()
            case Type.DIRECTORY_FORCED:
                self._remove_dir()
            case Type.PROCESS:
                self._end_process()

    def _remove_file(self) -> None:
        if not os.path.exists(self.value):
            pass  # if it does not exists, do nothing
        elif os.path.isdir(self.value):
            self.result = Result.ERROR
            self.detail = "Is a directory, not a file"
        else:
            self._remove()

    def _remove_dir(self) -> None:
        if not os.path.exists(self.value):
            pass  # if it does not exists, do nothing
        elif os.path.isfile(self.value):
            self.result = Result.ERROR
            self.detail = "Is a file, not a directory"
        elif self.type == Type.DIRECTORY and not is_dir_empty(self.value):
            self.result = Result.ERROR
            self.detail = "Directory is not empty"
        else:
            self._remove()

    def _remove(self) -> None:
        try:
            send2trash(self.value)
            self.result = Result.OK
        except PermissionError as e:
            self.result = Result.ERROR
            self.detail = str(e)

    def _end_process(self) -> None:
        proc_list = get_proc_list(self.value)

        if len(proc_list) > 0:
            self.result = Result.OK
            self.detail = "PID ="

            for proc in proc_list:
                try:
                    proc.terminate()
                    self.detail += f" {proc.pid},"
                except psutil.AccessDenied as e:
                    self.result = Result.ERROR
                    self.detail += f" {e.pid}(AccessDenied),"

            self.detail = self.detail.rstrip(",")

    def print(self, width: int) -> None:
        message = f" - {self.type} -> {self.result}"

        if self.detail is not None:
            message += f" : {self.detail}"

        print(f"{self.value.ljust(width, ' ')}{message}")


class ItemList:
    def __init__(self) -> None:
        self.items: list[Item] = []
        self.max_value_length: int = 0  # max length of all values added

    def add(self, type: Type, value: str) -> None:
        # if it is a path, normalize it
        if type in [Type.FILE, Type.DIRECTORY, Type.DIRECTORY_FORCED]:
            value = normit(value)

        self.items.append(Item(type, value))

        self.max_value_length = max(self.max_value_length, len(value))

    def process(self) -> None:
        for item in self.items:
            item.process()

    def print(self):
        for item in self.items:
            item.print(self.max_value_length)


parser = argparse.ArgumentParser(
    prog="seek_and_destroy",
    description="Remove files/directories and stop processes that are listed.",
)
args = parser.parse_args()


documents = userpaths.get_my_documents()  # type: ignore
videos = userpaths.get_my_videos()  # type: ignore

items = ItemList()

# Files
items.add(Type.FILE, "%UserProfile%/.bash_history")
items.add(Type.FILE, "%UserProfile%/.lesshst")
items.add(Type.FILE, "%UserProfile%/.python_history")

# Directories
items.add(Type.DIRECTORY, "%UserProfile%/.ms-ad/")
items.add(Type.DIRECTORY, f"{documents}/Modèles Office personnalisés/")
items.add(Type.DIRECTORY, f"{videos}/Captures/")

# Directories - OneDrive
items.add(Type.DIRECTORY, "%OneDrive%/Attachments/")
items.add(Type.DIRECTORY, "%OneDrive%/Enregistrements/")
items.add(Type.DIRECTORY, "%OneDrive%/Réunions/")

# Directories - forced
items.add(Type.DIRECTORY_FORCED, "%UserProfile%/.cache/")
items.add(Type.DIRECTORY_FORCED, "%UserProfile%/.idlerc/")
items.add(Type.DIRECTORY_FORCED, "%UserProfile%/.lemminx/")
items.add(Type.DIRECTORY_FORCED, "%UserProfile%/.thumbnails/")
items.add(Type.DIRECTORY_FORCED, "%UserProfile%/Favorites/")
items.add(Type.DIRECTORY_FORCED, "%UserProfile%/Oracle/")
items.add(Type.DIRECTORY_FORCED, "%UserProfile%/Searches/")
items.add(Type.DIRECTORY_FORCED, f"{documents}/Blocs-notes OneNote/")
items.add(Type.DIRECTORY_FORCED, f"{documents}/Copilot/")
items.add(Type.DIRECTORY_FORCED, f"{documents}/Dell/")
items.add(Type.DIRECTORY_FORCED, f"{documents}/plsqldoc/")

# Processes
items.add(Type.PROCESS, "AdobeCollabSync.exe")
items.add(Type.PROCESS, "ai.exe")
items.add(Type.PROCESS, "AppActions.exe")
items.add(Type.PROCESS, "CrossDeviceResume.exe")
items.add(Type.PROCESS, "CrossDeviceService.exe")
items.add(Type.PROCESS, "LockApp.exe")
items.add(Type.PROCESS, "msedge.exe")

items.process()
items.print()
