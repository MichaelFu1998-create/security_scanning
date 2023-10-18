def expand_words(self, line, width=60):
        """ Insert spaces between words until it is wide enough for `width`.
        """
        if not line.strip():
            return line
        # Word index, which word to insert on (cycles between 1->len(words))
        wordi = 1
        while len(strip_codes(line)) < width:
            wordendi = self.find_word_end(line, wordi)
            if wordendi < 0:
                # Reached the end?, try starting at the front again.
                wordi = 1
                wordendi = self.find_word_end(line, wordi)
            if wordendi < 0:
                # There are no spaces to expand, just prepend one.
                line = ''.join((' ', line))
            else:
                line = ' '.join((line[:wordendi], line[wordendi:]))
                wordi += 1

        # Don't push a single word all the way to the right.
        if ' ' not in strip_codes(line).strip():
            return line.replace(' ', '')
        return line