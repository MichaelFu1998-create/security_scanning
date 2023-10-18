def advance_past_chars(self, chars):
        """Advance the index past specific chars
        Args chars (list): list of characters to advance past

        Return substring that was advanced past
        """
        start_index = self.index
        while True:
            current_char = self.raw_text[self.index]
            self.index += 1
            if current_char in chars:
                break

            elif self.index == self.len:
                break

        return self.raw_text[start_index : self.index - 1]