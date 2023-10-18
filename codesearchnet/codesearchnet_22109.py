def new(self, mode):
        """
        Create a new instance of a game. Note, a mode MUST be provided and MUST be of
        type GameMode.

        :param mode: <required>

        """
        dw = DigitWord(wordtype=mode.digit_type)
        dw.random(mode.digits)

        self._key = str(uuid.uuid4())
        self._status = ""
        self._ttl = 3600
        self._answer = dw
        self._mode = mode
        self._guesses_remaining = mode.guesses_allowed
        self._guesses_made = 0