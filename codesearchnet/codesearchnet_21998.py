def _start_again_message(self, message=None):
        """Simple method to form a start again message and give the answer in readable form."""
        logging.debug("Start again message delivered: {}".format(message))
        the_answer = ', '.join(
            [str(d) for d in self.game.answer][:-1]
        ) + ', and ' + [str(d) for d in self.game.answer][-1]

        return "{0}{1} The correct answer was {2}. Please start a new game.".format(
            message,
            "." if message[-1] not in [".", ",", ";", ":", "!"] else "",
            the_answer
        )