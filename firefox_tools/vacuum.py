import os
import sqlite3
from pathlib import Path

from utils import file_size_to_str as sts
from utils import proc_is_running
from utils.colors import FG


def vacuum_profile(profile_path: str) -> None:
    if proc_is_running("firefox.exe") or proc_is_running("zen.exe"):
        print(f"{FG.RED}ERROR{FG.CLEAR} Could not vacuum, Firefox (or Zen) is running")
        return

    nb_files: int = 0
    total_before: int = 0
    total_after: int = 0

    for filename in Path(profile_path).glob("**/*.sqlite"):
        rel_path = os.path.relpath(filename, profile_path)
        size_before = os.path.getsize(filename)

        # skip suggest.sqlite because VACUUM raises an exception (no such collation sequence: i18n_collate)
        if rel_path == "suggest.sqlite":
            continue

        try:
            conn = sqlite3.connect(filename)
            conn.execute("VACUUM")
            conn.close()

            # if no exception, increase counters
            nb_files += 1
            total_before += size_before

            size_after = os.path.getsize(filename)
            total_after += size_after

            print(f"{rel_path} : {sts(size_before)} -> {sts(size_after)}")

        except sqlite3.OperationalError as e:
            print(f"{rel_path} {FG.RED}ERROR{FG.CLEAR}: {e}")

    saved_size = sts(total_before - total_after)
    print(f"""
Vacuumed {nb_files} files, {saved_size} saved ({sts(total_before)} -> {sts(total_after)})""")
