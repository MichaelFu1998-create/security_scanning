def _handle_auth_success(self, stream, success):
        """Handle successful authentication.

        Send <success/> and mark the stream peer authenticated.

        [receiver only]
        """
        if not self._check_authorization(success.properties, stream):
            element = ElementTree.Element(FAILURE_TAG)
            ElementTree.SubElement(element, SASL_QNP + "invalid-authzid")
            return True
        authzid = success.properties.get("authzid")
        if authzid:
            peer = JID(success.authzid)
        elif "username" in success.properties:
            peer = JID(success.properties["username"], stream.me.domain)
        else:
            # anonymous
            peer = None
        stream.set_peer_authenticated(peer, True)