import pytest

class TestCountSimbols:
    phrase = input("Set a phrase less 15 simbols: ")
    def test_length_phrase(self):
        assert len(self.phrase) < 15 , f'Phrase {self.phrase} more than 15 simbols '
