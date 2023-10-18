def _auth(self):
        """Authenticate on the server.

        [component only]"""
        if self.authenticated:
            self.__logger.debug("_auth: already authenticated")
            return
        self.__logger.debug("doing handshake...")
        hash_value=self._compute_handshake()
        n=common_root.newTextChild(None,"handshake",hash_value)
        self._write_node(n)
        n.unlinkNode()
        n.freeNode()
        self.__logger.debug("handshake hash sent.")