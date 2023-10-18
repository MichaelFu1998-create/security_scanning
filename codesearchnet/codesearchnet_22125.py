def guess(self, *args):
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
        self._validate_game_object(op="guess")

        logging.debug("Building return object")
        _return_results = {
            "cows": None,
            "bulls": None,
            "analysis": [],
            "status": ""
        }

        logging.debug("Check if game already won, lost, or too many tries.")
        if self._g.status.lower() == "won":
            _return_results["message"] = self._start_again("You already won!")
        elif self._g.status.lower() == "lost":
            _return_results["message"] = self._start_again("You have made too many guesses_allowed, you lost!")
        elif self._g.guesses_remaining < 1:
            _return_results["message"] = self._start_again("You have run out of tries, sorry!")
        elif self._g.ttl < time():
            _return_results["message"] = self._start_again("Sorry, you ran out of time to complete the puzzle!")
        else:
            logging.debug("Creating a DigitWord for the guess.")

            _wordtype = DigitWord.HEXDIGIT if self._g.mode.lower() == 'hex' else DigitWord.DIGIT
            guess = DigitWord(*args, wordtype=_wordtype)

            logging.debug("Validating guess.")
            self._g.guesses_remaining -= 1
            self._g.guesses_made += 1

            logging.debug("Initializing return object.")
            _return_results["analysis"] = []
            _return_results["cows"] = 0
            _return_results["bulls"] = 0

            logging.debug("Asking the underlying GameObject to compare itself to the guess.")
            for i in self._g.answer.compare(guess):
                logging.debug("Iteration of guesses_allowed. Processing guess {}".format(i.index))

                if i.match is True:
                    logging.debug("Bull found. +1")
                    _return_results["bulls"] += 1
                elif i.in_word is True:
                    logging.debug("Cow found. +1")
                    _return_results["cows"] += 1

                logging.debug("Add analysis to return object")
                _return_results["analysis"].append(i.get_object())

            logging.debug("Checking if game won or lost.")
            if _return_results["bulls"] == len(self._g.answer.word):
                logging.debug("Game was won.")
                self._g.status = "won"
                self._g.guesses_remaining = 0
                _return_results["message"] = "Well done! You won the game with your " \
                                             "answers {}".format(self._get_text_answer())
            elif self._g.guesses_remaining < 1:
                logging.debug("Game was lost.")
                self._g.status = "lost"
                _return_results["message"] = "Sorry, you lost! The correct answer was " \
                                             "{}".format(self._get_text_answer())
            _return_results["status"] = self._g.status

        logging.debug("Returning results.")
        return _return_results