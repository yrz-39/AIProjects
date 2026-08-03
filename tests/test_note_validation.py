from app import note_validation

def test_validate_note_strips_surrounding_whitespace():
    result=note_validation.validate_note("  链表是一种线性结构。  ")

    assert result =="链表是一种线性结构。"
