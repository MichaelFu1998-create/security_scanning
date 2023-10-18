def to_message(self):
        """
        Creates an error Acknowledgement message.
        The message's code and message are taken from this exception.

        :return: the message representing this exception
        """
        from .messages import ack
        return ack.Acknowledgement(self.code, self.args[0] if len(self.args) > 0 else '')