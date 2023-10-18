def receive(self, msg):
        """
        Returns a (receiver, msg) pair, where receiver is `None` if no route for
        the message was found, or otherwise an object with a `receive` method
        that can accept that `msg`.
        """
        x = self.routing
        while not isinstance(x, ActionList):
            if not x or not msg:
                return None, msg

            if not isinstance(x, dict):
                raise ValueError('Unexpected type %s' % type(x))

            _, value = msg.popitem(last=False)
            x = x.get(str(value))

        return x, msg