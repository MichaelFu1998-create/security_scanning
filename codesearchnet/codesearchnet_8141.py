def _receive(self, msg):
        """
        Receive a message from the input source and perhaps raise an Exception.
        """
        msg = self._convert(msg)
        if msg is None:
            return

        str_msg = self.verbose and self._msg_to_str(msg)
        if self.verbose and log.is_debug():
            log.debug('Message %s', str_msg)

        if self.pre_routing:
            self.pre_routing.receive(msg)

        receiver, msg = self.routing.receive(msg)
        if receiver:
            receiver.receive(msg)
            if self.verbose:
                log.info('Routed message %s (%s) to %s', str_msg[:128], msg,
                         repr(receiver))