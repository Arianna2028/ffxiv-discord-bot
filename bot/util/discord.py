def parse_character_name(full_name: str) -> str:
    """From a full Discord nickname in the format ``Name (First Last)``
    where Name is the human's name and First Last are the in-game character
    name, retrieve just the character name.

    Raises:
        ValueError: if the provided ``full_name`` does not match the expected
            format
    """

    parts = full_name.replace("(", "").replace(")", "").split(" ")
    if len(parts) != 3:
        raise ValueError(f"Unexpected name format: {full_name}")
    _, first, last = parts
    return f"{first} {last}"
