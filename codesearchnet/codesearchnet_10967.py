def _translate_string(self, data, length):
        """Translate string into character texture positions"""
        for index, char in enumerate(data):
            if index == length:
                break

            yield self._meta.characters - 1 - self._ct[char]