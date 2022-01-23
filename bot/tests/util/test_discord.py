import pytest

from bot.util.discord import parse_character_name


class TestDiscord:
    @pytest.mark.parametrize(
        "name",
        [
            "First Last",
            "First",
            "(First Last)",
            "(First)",
            "Real (First)",
            "(First) Real",
        ],
    )
    def test_parse_character_name_errors(self, name: str):
        with pytest.raises(ValueError):
            parse_character_name(name)

    def test_parse_character_name(self):
        assert parse_character_name("Real (First Last)") == "First Last"
