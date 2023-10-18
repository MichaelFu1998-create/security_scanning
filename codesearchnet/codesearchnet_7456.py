def correct(self, text: str, srctext=None) -> str:
        """Automatically apply suggestions to the text."""
        return correct(text, self.check(text, srctext))