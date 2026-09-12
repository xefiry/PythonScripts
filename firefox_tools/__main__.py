import argparse
import glob
import os

from utils import choose_from, normit

from .permissions import print_permissions
from .search_engines import print_search_engines
from .vacuum import vacuum_profile

# paths to search profiles
SEARCH_PATHS = ["%AppData%/Mozilla/Firefox/Profiles/", "%AppData%/zen/Profiles/"]


def get_profiles() -> list[str]:
    result: list[str] = []

    # search for all permissions.sqlite files in search paths to find profiles dirs
    for path in SEARCH_PATHS:
        path = normit(path)
        for file in glob.glob(f"{path}/**/permissions.sqlite"):
            result.append(normit(os.path.dirname(file)))

    return result


def main():
    parser = argparse.ArgumentParser(
        prog="firefox_tools",
        description="""Tools for Firefox (and Zen) : print permissions & search engines, vacuum profiles.
If no option is set, defaults to printing permissions & search engines.""",
        formatter_class=argparse.RawTextHelpFormatter,
    )
    parser.add_argument(
        "-p", "--permissions", action="store_true", help="only print permissions"
    )
    parser.add_argument(
        "-s", "--search_engines", action="store_true", help="only print search engines"
    )
    parser.add_argument(
        "-v", "--vacuum", action="store_true", help="vacuum .db files in the profiles"
    )
    parser.add_argument("-i", "--input", help="use this value for the prompt")
    args = parser.parse_args()

    # if no option is set, put -p and -s to true
    if not (args.permissions or args.search_engines or args.vacuum):
        args.permissions = True
        args.search_engines = True

    profiles = choose_from(get_profiles(), args.input)
    for index, profile in enumerate(profiles):
        if index != 0:
            print(f"\n{'-' * 80}\n")
        print(f"Profile : {profile}\n")

        if args.permissions:
            print(">> Permissions\n")
            print_permissions(os.path.join(profile, "permissions.sqlite"))
            print()

        if args.search_engines:
            print(">> Search engines\n")
            print_search_engines(os.path.join(profile, "search.json.mozlz4"))
            print()

        if args.vacuum:
            print(">> Vacuumming profile\n")
            vacuum_profile(profile)
            print()


if __name__ == "__main__":
    main()
