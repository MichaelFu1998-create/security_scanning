def get_messages_payload(self, socket, timeout=None):
        """This will fetch the messages from the Socket's queue, and if
        there are many messes, pack multiple messages in one payload and return
        """
        try:
            msgs = socket.get_multiple_client_msgs(timeout=timeout)
            data = self.encode_payload(msgs)
        except Empty:
            data = ""
        return data