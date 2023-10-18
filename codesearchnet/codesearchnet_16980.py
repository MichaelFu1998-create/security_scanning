def tell(self, message, sender=no_sender):
        """ Send a message to this actor. Asynchronous fire-and-forget.

        :param message: The message to send.
        :type message: Any

        :param sender: The sender of the message. If provided it will be made
            available to the receiving actor via the :attr:`Actor.sender` attribute.
        :type sender: :class:`Actor`
        """
        if sender is not no_sender and not isinstance(sender, ActorRef):
            raise ValueError("Sender must be actor reference")

        self._cell.send_message(message, sender)