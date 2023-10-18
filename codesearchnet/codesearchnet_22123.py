def load_game(self, jsonstr):
        """
        load_game() takes a JSON string representing a game object and calls the underlying
        game object (_g) to load the JSON. The underlying object will handle schema validation
        and transformation.

        :param jsonstr: A valid JSON string representing a GameObject (see above)

        :return: None

        """
        logging.debug("load_game called.")
        logging.debug("Creating empty GameObject.")
        self._g = GameObject()

        logging.debug("Calling from_json with {}.".format(jsonstr))
        self._g.from_json(jsonstr=jsonstr)