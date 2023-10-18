def guess(self, *args):
        self._validate()
        """
        guess() allows a guess to be made. Before the guess is made, the method
        checks to see if the game has been won, lost, or there are no tries
        remaining. It then creates a return object stating the number of bulls
        (direct matches), cows (indirect matches), an analysis of the guess (a
        list of analysis objects), and a status.

        :param args: any number of integers (or string representations of integers)
        to the number of Digits in the answer; i.e. in normal mode, there would be
        a DigitWord to guess of 4 digits, so guess would expect guess(1, 2, 3, 4)
        and a shorter (guess(1, 2)) or longer (guess(1, 2, 3, 4, 5)) sequence will
        raise an exception.

        :return: a JSON object containing the analysis of the guess:

        {
            "cows": {"type": "integer"},
            "bulls": {"type": "integer"},
            "analysis": {"type": "array of DigitWordAnalysis"},
            "status": {"type": "string"}
        }

        """
        logging.debug("guess called.")
        logging.debug("Validating game object")
        self._validate(op="guess")

        logging.debug("Building return object")
        _return_results = {
            "cows": None,
            "bulls": None,
            "analysis": [],
            "status": ""
        }

        logging.debug("Check if game already won, lost, or too many tries.")
        if self._game.status == GameObject.GAME_WON:
            _return_results["message"] = self._start_again("You already won!")
        elif self._game.status == GameObject.GAME_LOST:
            _return_results["message"] = self._start_again("You have made too many guesses, you lost!")
        elif self._game.guesses_remaining < 1:
            _return_results["message"] = self._start_again("You have run out of tries, sorry!")
        else:
            logging.debug("Creating a DigitWord for the guess.")

            _mode = self._load_mode(self._game.mode)
            guess = DigitWord(*args, wordtype=_mode.digit_type)

            logging.debug("Validating guess.")
            self._game.guesses_remaining -= 1
            self._game.guesses_made += 1

            logging.debug("Initializing return object.")
            _return_results["analysis"] = []
            _return_results["cows"] = 0
            _return_results["bulls"] = 0

            logging.debug("Asking the underlying GameObject to compare itself to the guess.")
            for i in self._game.answer.compare(guess):
                logging.debug("Iteration of guesses. Processing guess {}".format(i.index))

                if i.match is True:
                    logging.debug("Bull found. +1")
                    _return_results["bulls"] += 1
                elif i.in_word is True:
                    logging.debug("Cow found. +1")
                    _return_results["cows"] += 1

                logging.debug("Add analysis to return object")
                _return_results["analysis"].append(i.get_object())

            logging.debug("Checking if game won or lost.")
            if _return_results["bulls"] == len(self._game.answer.word):
                logging.debug("Game was won.")
                self._game.status = GameObject.GAME_WON
                self._game.guesses_remaining = 0
                _return_results["message"] = "Well done! You won the game with your " \
                                             "answers {}".format(self._game.answer_str)
            elif self._game.guesses_remaining < 1:
                logging.debug("Game was lost.")
                self._game.status = GameObject.GAME_LOST
                _return_results["message"] = "Sorry, you lost! The correct answer was " \
                                             "{}".format(self._game.answer_str)
            _return_results["status"] = self._game.status

        logging.debug("Returning results.")
        return _return_results