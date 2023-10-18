def _isSingleCharacter(keychr):
        """Check whether given keyboard character is a single character.

        Parameters: key character which will be checked.
        Returns: True when given key character is a single character.
        """
        if not keychr:
            return False
        # Regular character case.
        if len(keychr) == 1:
            return True
        # Tagged character case.
        return keychr.count('<') == 1 and keychr.count('>') == 1 and \
               keychr[0] == '<' and keychr[-1] == '>'