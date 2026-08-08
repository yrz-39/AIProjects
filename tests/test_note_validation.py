from app import note_validation


def test_validate_note_strips_surrounding_whitespace():
    result = note_validation.validate_note("  链表是一种线性结构。  ")
    assert result == "链表是一种线性结构。"


def test_validate_note_strips_tab_and_newline():
    result = note_validation.validate_note("链表\t是线性结构\n")
    assert result == "链表\t是线性结构"


def test_validate_note_empty_string():
    assert note_validation.validate_note("") == ""


def test_validate_note_all_whitespace():
    assert note_validation.validate_note(" \t\n ") == ""


def test_validate_note_keeps_inner_whitespace():
    result = note_validation.validate_note("链表 是 线性结构")
    assert result == "链表 是 线性结构"


def test_validate_note_no_whitespace_unchanged():
    assert note_validation.validate_note("链表") == "链表"
