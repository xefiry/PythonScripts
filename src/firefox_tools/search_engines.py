import json

import lz4.block


class SearchEngine:
    order: int
    name: str
    alias: str
    url: str
    post: str
    suggestion: str

    def __init__(self, data: dict) -> None:
        if "_iconMapObj" in data:
            data.pop("_iconMapObj")

        self.order = data["_metaData"]["order"]
        self.name = data["_name"]
        self.alias = data["_metaData"]["alias"]

        for url in data["_urls"]:
            template = url["template"].replace("{searchTerms}", "%s")

            if url.get("type") == "application/x-suggestions+json":
                self.suggestion = template
            else:
                self.url = template

            # if url method is post, concatenate params as a usable string
            if url.get("method") == "POST":
                self.post = decode_post(url["params"])

    def __str__(self) -> str:
        result: str = ""

        # result += f"\n{self.order}"
        result += f"\n{self.name}"
        result += f"\n{self.alias}"
        if hasattr(self, "url"):
            result += f"\n{self.url}"
        if hasattr(self, "post"):
            result += f"\nPOST: {self.post}"
        if hasattr(self, "suggestion"):
            result += f"\nSUGGESTION: {self.suggestion}"

        return result

    def __lt__(self, other) -> bool:
        return self.order < other.order


def decode_post(input: dict) -> str:
    params = []
    for param in input:
        key = param["name"]
        value = param["value"].replace("{searchTerms}", "%s")
        params.append(f"{key}={value}")
    params_string = "&".join(params)

    return params_string


def print_all(input_file: str):
    with open(input_file, "rb") as file:
        if file.read(8) != b"mozLz40\0":
            raise OSError("Invalid magic number")

        file_data = file.read()

    decoded_data = lz4.block.decompress(file_data)
    json_str = decoded_data.decode("utf-8")
    json_data = json.loads(json_str)
    engines_list: list[SearchEngine] = []

    for engine_data in json_data["engines"]:
        # if it is not a user engines (default or extension engine)
        if engine_data.get("_loadPath") != "[user]":
            continue

        engines_list.append(SearchEngine(engine_data))

    print(f"version = {json_data['version']}")

    if len(engines_list) == 0:
        print("No search engine")
        return

    engines_list.sort()

    for engine in engines_list:
        print(engine)
