import pytest

import utils

VALUES = ["a", "b", "c", "d", "e", "f", "g", "h", "i", "j"]


def test_pick_choices_empty():
    assert utils.pick_choices(5, "") == []
    assert utils.pick_choices(5, "  * ") == [0, 1, 2, 3, 4]


def test_pick_choices_all():
    assert utils.pick_choices(5, "*") == [0, 1, 2, 3, 4]
    assert utils.pick_choices(5, "  * ") == [0, 1, 2, 3, 4]


def test_pick_choices_single():
    assert utils.pick_choices(5, "0") == [0]
    assert utils.pick_choices(5, "2") == [2]
    assert utils.pick_choices(5, "4") == [4]


def test_pick_choices_multi():
    assert utils.pick_choices(5, "1, 3, 4") == [1, 3, 4]
    assert utils.pick_choices(5, "4, 3, 1") == [1, 3, 4]
    assert utils.pick_choices(10, "9, 4, 5, 2") == [2, 4, 5, 9]
    assert utils.pick_choices(10, "9,,,,, 4, 5, 2") == [2, 4, 5, 9]


def test_pick_choices_range():
    assert utils.pick_choices(10, "0-3") == [0, 1, 2, 3]
    assert utils.pick_choices(10, "1-2") == [1, 2]


def test_pick_choices_combinaison():
    assert utils.pick_choices(15, "1, 9, 2-5, 10-12") == [1, 2, 3, 4, 5, 9, 10, 11, 12]


def test_pick_choices_errors():
    with pytest.raises(ValueError):
        utils.pick_choices(3, "3")

    with pytest.raises(ValueError):
        utils.pick_choices(3, "1-3")


def test_choose_from_empty():
    assert utils.choose_from(VALUES, "") == []


def test_choose_from_all():
    assert utils.choose_from(VALUES, "*") == VALUES


def test_choose_from_single():
    assert utils.choose_from(VALUES, "0") == ["a"]
    assert utils.choose_from(VALUES, "5") == ["f"]
    assert utils.choose_from(VALUES, "8") == ["i"]


def test_choose_from_multi():
    assert utils.choose_from(VALUES, "1, 3, 4") == ["b", "d", "e"]
    assert utils.choose_from(VALUES, "4, 3, 1") == ["b", "d", "e"]
    assert utils.choose_from(VALUES, "9, 4, 5, 2") == ["c", "e", "f", "j"]
    assert utils.choose_from(VALUES, "9,,,,, 4, 5, 2") == ["c", "e", "f", "j"]


def test_choose_from_range():
    assert utils.choose_from(VALUES, "0-3") == ["a", "b", "c", "d"]
    assert utils.choose_from(VALUES, "1-2") == ["b", "c"]


def test_choose_from_combinaison():
    expected = ["a", "c", "d", "e", "g", "h", "j"]
    assert utils.choose_from(VALUES, "0, 9, 2-4, 6-7") == expected


def test_choose_from_errors():
    with pytest.raises(ValueError):
        assert utils.choose_from(VALUES, "10")

    with pytest.raises(ValueError):
        assert utils.choose_from(VALUES, "1-10")
