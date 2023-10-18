def _process_sasl_success(self, stream, element):
        """Process incoming <sasl:success/> element.

        [initiating entity only]

        """
        if not self.authenticator:
            logger.debug("Unexpected SASL response")
            return False

        content = element.text

        if content:
            data = a2b_base64(content.encode("us-ascii"))
        else:
            data = None
        ret = self.authenticator.finish(data)
        if isinstance(ret, sasl.Success):
            logger.debug("SASL authentication succeeded")
            authzid = ret.properties.get("authzid")
            if authzid:
                me = JID(authzid)
            elif "username" in ret.properties:
                # FIXME: other rules for server
                me = JID(ret.properties["username"], stream.peer.domain)
            else:
                me = None
            stream.set_authenticated(me, True)
        else:
            logger.debug("SASL authentication failed")
            raise SASLAuthenticationFailed("Additional success data"
                                                        " procesing failed")
        return True