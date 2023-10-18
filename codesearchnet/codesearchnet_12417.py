def _validate_checksum(self):
        """Given a mnemonic word string, confirm seed checksum (last word) matches the computed checksum.

        :rtype: bool
        """
        phrase = self.phrase.split(" ")
        if self.word_list.get_checksum(self.phrase) == phrase[-1]:
            return True
        raise ValueError("Invalid checksum")