import argparse
import glob
import os

from utils import choose_from, normit

from .permissions import print_all as print_permissions
from .search_engines import print_all as print_search_engines

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
        description="Print permissions and serach engines on Firefox (and Zen) profiles.",
    )
    parser.add_argument(
        "-p", "--permissions", action="store_true", help="only print permissions"
    )
    parser.add_argument(
        "-s", "--search_engines", action="store_true", help="only print search engines"
    )
    parser.add_argument("-i", "--input", help="use this value for the prompt")
    args = parser.parse_args()

    # neither -p nor -s is set, put them both to true
    if not (args.permissions or args.search_engines):
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

        if args.permissions and args.search_engines:
            print()

        if args.search_engines:
            print(">> Search engines\n")
            print_search_engines(os.path.join(profile, "search.json.mozlz4"))


if __name__ == "__main__":
    main()
