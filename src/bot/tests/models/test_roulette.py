import pytest

from bot.models.roulette import RouletteType


class TestRoulette:
    def test_roulette_type(self):
        assert RouletteType("leveling") == RouletteType.LEVELING
        assert RouletteType("trial") == RouletteType.TRIAL

        with pytest.raises(ValueError):
            RouletteType("bogus")
