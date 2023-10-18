def find_probable_year_index(self, tokens):
        """
        attempt to deduce if a pre 100 year was lost
         due to padded zeros being taken off
        """
        for index, token in enumerate(self):
            potential_year_tokens = _ymd.find_potential_year_tokens(
                token, tokens)
            if len(potential_year_tokens) == 1 and len(potential_year_tokens[0]) > 2:
                return index