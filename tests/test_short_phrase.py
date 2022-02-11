class TestShortPhrase:
    def test_short_phrase(self):
        phrase = input("Set a phrase: ")

        assert len(phrase) < 15, f"The length of given phrase '{phrase}' is >= 15 characters"
