def set_stream(self,stream):
        """
        Change the stream assigned to `self`.

        :Parameters:
            - `stream`: the new stream to be assigned to `self`.
        :Types:
            - `stream`: `pyxmpp.stream.Stream`
        """
        self.jid=stream.me
        self.stream=stream
        for r in self.rooms.values():
            r.set_stream(stream)