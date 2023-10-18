def _relay_message(self, message):
        """
        Relay messages from the forum on the server to the client represented 
        by this actor.
        """
        info("relaying message: {message}")

        if not message.was_sent_by(self._id_factory):
            self.pipe.send(message)
            self.pipe.deliver()