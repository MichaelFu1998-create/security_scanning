def _try_auth(self):
        """Try to authenticate using the first one of allowed authentication
        methods left.

        [client only]"""
        if self.authenticated:
            self.__logger.debug("try_auth: already authenticated")
            return
        self.__logger.debug("trying auth: %r" % (self._auth_methods_left,))
        if not self._auth_methods_left:
            raise LegacyAuthenticationError("No allowed authentication methods available")
        method=self._auth_methods_left[0]
        if method.startswith("sasl:"):
            return ClientStream._try_auth(self)
        elif method not in ("plain","digest"):
            self._auth_methods_left.pop(0)
            self.__logger.debug("Skipping unknown auth method: %s" % method)
            return self._try_auth()
        elif self.available_auth_methods is not None:
            if method in self.available_auth_methods:
                self._auth_methods_left.pop(0)
                self.auth_method_used=method
                if method=="digest":
                    self._digest_auth_stage2(self.auth_stanza)
                else:
                    self._plain_auth_stage2(self.auth_stanza)
                self.auth_stanza=None
                return
            else:
                self.__logger.debug("Skipping unavailable auth method: %s" % method)
        else:
            self._auth_stage1()