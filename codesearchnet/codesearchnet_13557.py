def set_stream(self,stream):
        """
        Called when current stream changes.

        Mark the room not joined and inform `self.handler` that it was left.

        :Parameters:
            - `stream`: the new stream.
        :Types:
            - `stream`: `pyxmpp.stream.Stream`
        """
        _unused = stream
        if self.joined and self.handler:
            self.handler.user_left(self.me,None)
        self.joined=False