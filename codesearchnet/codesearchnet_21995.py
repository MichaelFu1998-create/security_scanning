def guess(self, *args):
        """
        Make a guess, comparing the hidden object to a set of provided digits. The digits should
        be passed as a set of arguments, e.g:

        * for a normal game: 0, 1, 2, 3
        * for a hex game: 0xA, 0xB, 5, 4
        * alternate for hex game: 'A', 'b', 5, 4

        :param args: An iterable of digits (int or str)
        :return: A dictionary object detailing the analysis and results of the guess
        """

        if self.game is None:
            raise ValueError("The Game is unexpectedly undefined!")

        response_object = {
            "bulls": None,
            "cows": None,
            "analysis": None,
            "status": None
        }

        if self.game.status == self.GAME_WON:
            response_object["status"] = \
                self._start_again_message("You already won!")
        elif self.game.status == self.GAME_LOST:
            response_object["status"] = \
                self._start_again_message("You already lost!")
        elif self.game.guesses_remaining < 1:
            response_object["status"] = \
                self._start_again_message("You've made too many guesses")
        else:
            guess_made = DigitWord(*args, wordtype=self.game.mode.digit_type)
            comparison = self.game.answer.compare(guess_made)

            self.game.guesses_made += 1
            response_object["bulls"] = 0
            response_object["cows"] = 0
            response_object["analysis"] = []

            for comparison_object in comparison:
                if comparison_object.match:
                    response_object["bulls"] += 1
                elif comparison_object.in_word:
                    response_object["cows"] += 1
                response_object["analysis"].append(comparison_object.get_object())

            if response_object["bulls"] == self.game.mode.digits:
                self.game.status = self.GAME_WON
                self.game.guesses_made = self.game.mode.guesses_allowed
                response_object["status"] = self._start_again_message(
                    "Congratulations, you win!"
                )
            elif self.game.guesses_remaining < 1:
                self.game.status = self.GAME_LOST
                response_object["status"] = self._start_again_message(
                    "Sorry, you lost!"
                )

        return response_object