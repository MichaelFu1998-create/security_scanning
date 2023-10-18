def _validate_game_object(self, op="unknown"):
        """
        A helper method to provide validation of the game object (_g). If the
        game object does not exist or if (for any reason) the object is not a GameObject,
        then an exception will be raised.

        :param op: A string describing the operation (e.g. guess, save, etc.) taking place
        :return: Nothing
        """
        if self._g is None:
            raise ValueError(
                "Game must be instantiated properly before using - call new_game() "
                "or load_game(jsonstr='{...}')"
            )
        if not isinstance(self._g, GameObject):
            raise TypeError(
                "Unexpected error during {0}! GameObject (_g) is not a GameObject!".format(op)
            )