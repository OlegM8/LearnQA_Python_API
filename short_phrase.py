

class TestShortPhrase:
    phrase = input("Set a phrase: ")

    def test_short_phrase(self):
        assert len(self.phrase) < 15, "The phrase is longer than 14 characters"
