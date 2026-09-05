import os


def normit(path: str) -> str:
    return os.path.normpath(os.path.expandvars(path))


def pick_choices(max_index: int, _input: str | None = None) -> list[int]:
    """Ask the user to enter indexes. Usefull to pick elements in a list.

    Examples of input with output
    - all : * -> [0, 1, 2, ..., max-1]
    - single number : 3 -> [3]
    - multiple numbers : 1, 7, 4 -> [1, 7, 4]
    - ranges : 2-5 -> [2, 3, 4, 5]
    - combinaison : 1, 9, 2-5, 10-12 -> [1, 2, 3, 4, 5, 9, 10, 11, 12]

    Args:
        max (int): max value for index (excluded). Example, if max = 5, allowed numbers will be between 0 and 4.
        _input (str, optional): If set, it will be used as input (replace the call to input in the function).

    Returns:
        list[int]: A list of indexes, sorted, without duplicates.
    """

    result: list[int] = []

    if _input is None:
        _input = input(
            f"Pick indexes, min = 0, max = {max_index - 1}, * for all (examples : 1, 3, 5-8) \n> "
        )

    # remove all spaces in the input
    _input = _input.replace(" ", "")

    if _input == "":
        return []
    elif _input == "*":
        return list(range(max_index))

    for i in _input.split(","):
        if i == "":  # ignore empty values
            pass
        elif "-" in i:  # case a-b
            _spl = i.split("-", 1)
            _min = int(_spl[0])
            _max = int(_spl[1]) + 1

            result += range(_min, _max)
        else:
            result.append(int(i))

    result.sort()

    max_val = max(result)
    if max_val >= max_index:
        raise ValueError(
            f"Max value ({max_val}) exceds the maximum allowed ({max_index})"
        )

    return result


def choose_from(values: list[str], _input: str | None = None) -> list[str]:
    """Ask the user to choose from a list of values.

    Args:
        values (list[str]): The values to choose from
        _input (str, optional): If set, it will be used as input (replace the call to input in the function).

    Returns:
        list[str]: A list of choosed values (inputed indexes are sorted and de-duplicated).
    """

    result: list[str] = []

    for i, j in enumerate(values):
        print(f"{i} - {j}")
    print()

    choices = pick_choices(len(values), _input)

    for i in choices:
        result.append(values[i])

    return result


if __name__ == "__main__":
    print(choose_from(["a", "b", "c"]))
