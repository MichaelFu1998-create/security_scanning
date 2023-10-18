def save_game(self):
        """
        save_game() asks the underlying game object (_g) to dump the contents of
        itself as JSON and then returns the JSON to

        :return: A JSON representation of the game object

        """
        logging.debug("save_game called.")
        logging.debug("Validating game object")
        self._validate_game_object(op="save_game")

        logging.debug("Dumping JSON from GameObject")
        return self._g.to_json()