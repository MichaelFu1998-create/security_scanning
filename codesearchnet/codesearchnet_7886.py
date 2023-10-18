def get_multiple_client_msgs(self, **kwargs):
        """Get multiple messages, in case we're going through the various
        XHR-polling methods, on which we can pack more than one message if the
        rate is high, and encode the payload for the HTTP channel."""
        client_queue = self.client_queue
        msgs = [client_queue.get(**kwargs)]
        while client_queue.qsize():
            msgs.append(client_queue.get())
        return msgs