def _start_again(self, message=None):
        """Simple method to form a start again message and give the answer in readable form."""
        logging.debug("Start again message delivered: {}".format(message))
        the_answer = self._get_text_answer()

        return "{0} The correct answer was {1}. Please start a new game.".format(
            message,
            the_answer
        )