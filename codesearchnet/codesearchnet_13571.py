def request_instant_room(self):
        """
        Request an "instant room" -- the default configuration for a MUC room.

        :return: id of the request stanza.
        :returntype: `unicode`
        """
        if self.configured:
            raise RuntimeError("Instant room may be requested for unconfigured room only")
        form = Form("submit")
        return self.configure_room(form)