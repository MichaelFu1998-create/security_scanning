def dump(self):
        """
        Dump (return) a dict representation of the GameObject. This is a Python
        dict and is NOT serialized. NB: the answer (a DigitWord object) and the
        mode (a GameMode object) are converted to python objects of a list and
        dict respectively.

        :return: python <dict> of the GameObject as detailed above.
        """

        return {
            "key": self._key,
            "status": self._status,
            "ttl": self._ttl,
            "answer": self._answer.word,
            "mode": self._mode.dump(),
            "guesses_made": self._guesses_made
        }