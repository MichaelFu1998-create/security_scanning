def fseq(self, client, message):
        """
        fseq messages associate a unique frame id with a set of set
        and alive messages
        """
        client.last_frame = client.current_frame
        client.current_frame = message[3]