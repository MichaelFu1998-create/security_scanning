def load(self, game_json=None, mode=None):
        """
        Load a game from a serialized JSON representation. The game expects a well defined
        structure as follows (Note JSON string format):

        '{
            "guesses_made": int,
            "key": "str:a 4 word",
            "status": "str: one of playing, won, lost",
            "mode": {
                "digits": int,
                "digit_type": DigitWord.DIGIT | DigitWord.HEXDIGIT,
                "mode": GameMode(),
                "priority": int,
                "help_text": str,
                "instruction_text": str,
                "guesses_allowed": int
            },
            "ttl": int,
            "answer": [int|str0, int|str1, ..., int|strN]
        }'

        * "mode" will be cast to a GameMode object
        * "answer" will be cast to a DigitWord object

        :param game_json: The source JSON - MUST be a string
        :param mode: A mode (str or GameMode) for the game being loaded
        :return: A game object
        """

        if game_json is None:    # New game_json
            if mode is not None:
                if isinstance(mode, str):
                    _game_object = GameObject(mode=self._match_mode(mode=mode))
                elif isinstance(mode, GameMode):
                    _game_object = GameObject(mode=mode)
                else:
                    raise TypeError("Game mode must be a GameMode or string")
            else:
                _game_object = GameObject(mode=self._game_modes[0])
            _game_object.status = self.GAME_PLAYING
        else:
            if not isinstance(game_json, str):
                raise TypeError("Game must be passed as a serialized JSON string.")

            game_dict = json.loads(game_json)

            if not 'mode' in game_dict:
                raise ValueError("Mode is not provided in JSON; game_json cannot be loaded!")

            _mode = GameMode(**game_dict["mode"])
            _game_object = GameObject(mode=_mode, source_game=game_dict)

        self.game = copy.deepcopy(_game_object)