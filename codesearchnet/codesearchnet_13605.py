def _connect(self,server=None,port=None):
        """Same as `ComponentStream.connect` but assume `self.lock` is acquired."""
        if self.me.node or self.me.resource:
            raise Value("Component JID may have only domain defined")
        if not server:
            server=self.server
        if not port:
            port=self.port
        if not server or not port:
            raise ValueError("Server or port not given")
        Stream._connect(self,server,port,None,self.me)