def new_game(self, mode=None):
        """
        new_game() creates a new game. Docs TBC.

        :return: JSON String containing the game object.

        """

        # Create a placeholder Game object
        self._g = GameObject()

        # Validate game mode
        _mode = mode or "normal"
        logging.debug("new_game: requesting mode {}".format(_mode))

        mode_info = self._g.get_game_type(gametype=_mode)
        logging.debug("mode_info: {} (Type: {})".format(mode_info, type(mode_info)))

        if not mode_info:
            self._g = None
            raise ValueError('The mode passed ({}) is not supported.'.format(_mode))

        logging.debug("Creating a DigitWord (type {})".format(mode_info.digitType))
        dw = DigitWord(wordtype=mode_info.digitType)
        dw.random(mode_info.digits)

        logging.debug("Randomized DigitWord. Value is {}.".format(dw.word))

        _game = {
            "key": str(uuid.uuid4()),
            "status": "playing",
            "ttl": int(time()) + 3600,
            "answer": dw.word,
            "mode": _mode,
            "guesses_remaining": mode_info.guesses_allowed,
            "guesses_made": 0
        }
        logging.debug("Game being created: {}".format(_game))

        self._g.from_json(jsonstr=json.dumps(_game))
        return self._g.to_json()