import sqlite3
import time

SQL_QUERY = """
SELECT m.type,
       m.origin,
       m.permission,
       m.expireType,
       m.expireTime,
       m.modificationTime
  FROM moz_perms m
 WHERE m.type not in ('storageAccessAPI', 'WebExtensions-unlimitedStorage', 'persistent-storage', 'highValueCOOP')
   AND m.type not like '3rdPartyStorage^%'
 ORDER BY m.type,
          m.origin;
"""


def timstamp_to_date(timestamp: int) -> str:
    format = "%Y-%m-%d %H:%M:%S"

    if timestamp == 0:
        return "N/A"
    else:
        return time.strftime(format, time.gmtime(timestamp / 1000))


def print_permissions(db_path: str) -> None:
    permissions: list[list[str]] = []

    con = sqlite3.connect(db_path)
    cur = con.cursor()

    for row in cur.execute(SQL_QUERY):
        row_type = row[0]
        row_origin = row[1]
        row_permission = row[2]
        row_expireType = row[3]
        row_expireTime = timstamp_to_date(row[4])
        row_modTime = timstamp_to_date(row[5])

        permissions.append(
            [
                row_type,
                row_origin,
                row_permission,
                row_expireType,
                row_expireTime,
                row_modTime,
            ]
        )

    cur.close()
    con.close()

    max_width = 6  # length of 'origin'
    prev_type = ""

    for perm in permissions:
        max_width = max(max_width, len(perm[1]))

    print(
        f"{'origin'.ljust(max_width)}  permission  expireType  expireTime           modificationTime"
    )

    for perm in permissions:
        if prev_type != perm[0]:
            prev_type = perm[0]
            print(perm[0])

        print(
            f"    {perm[1].ljust(max_width)}  {perm[2]}           {perm[3]}           "
            f"{perm[4].ljust(19)}  {perm[5].ljust(19)}"
        )
