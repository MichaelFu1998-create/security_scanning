def load_modes(self, input_modes=None):
        """
        Loads modes (GameMode objects) to be supported by the game object. Four default
        modes are provided (normal, easy, hard, and hex) but others could be provided
        either by calling load_modes directly or passing a list of GameMode objects to
        the instantiation call.

        :param input_modes: A list of GameMode objects; nb: even if only one new GameMode
        object is provided, it MUST be passed as a list - for example, passing GameMode gm1
        would require passing [gm1] NOT gm1.

        :return: A list of GameMode objects (both defaults and any added).
        """

        # Set default game modes
        _modes = [
            GameMode(
                mode="normal", priority=2, digits=4, digit_type=DigitWord.DIGIT, guesses_allowed=10
            ),
            GameMode(
                mode="easy", priority=1, digits=3, digit_type=DigitWord.DIGIT, guesses_allowed=6
            ),
            GameMode(
                mode="hard", priority=3, digits=6, digit_type=DigitWord.DIGIT, guesses_allowed=6
            ),
            GameMode(
                mode="hex", priority=4, digits=4, digit_type=DigitWord.HEXDIGIT, guesses_allowed=10
            )
        ]

        if input_modes is not None:
            if not isinstance(input_modes, list):
                raise TypeError("Expected list of input_modes")

            for mode in input_modes:
                if not isinstance(mode, GameMode):
                    raise TypeError("Expected list to contain only GameMode objects")
                _modes.append(mode)

        self._game_modes = copy.deepcopy(_modes)