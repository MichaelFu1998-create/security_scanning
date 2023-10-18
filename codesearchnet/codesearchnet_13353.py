def send(self, stanza):
        """Send a stanza somwhere.

        The default implementation sends it via the `uplink` if it is defined
        or raises the `NoRouteError`.

        :Parameters:
            - `stanza`: the stanza to send.
        :Types:
            - `stanza`: `pyxmpp.stanza.Stanza`"""
        if self.uplink:
            self.uplink.send(stanza)
        else:
            raise NoRouteError("No route for stanza")