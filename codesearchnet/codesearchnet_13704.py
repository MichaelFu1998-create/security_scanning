def auth_properties(self):
        """Authentication properties of the stream.

        Derived from the transport with 'local-jid' and 'service-type' added.
        """
        props = dict(self.settings["extra_auth_properties"])
        if self.transport:
            props.update(self.transport.auth_properties)
        props["local-jid"] = self.me
        props["service-type"] = "xmpp"
        return props