from app import repositories as repo
from app import llm_client

def generate_for_note(note_id: int, mode: str) -> dict|None:
    note = repo.get_note(note_id)
    if not note:
        return None
    result = llm_client.generate(note,mode)

    generation_id= repo.add_generation(note_id, mode, result)

    return {
        "id": generation_id,
        "note_id": note_id,
        "mode": mode,
        "result": result,
    }

