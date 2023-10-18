def connect(self,server=None,port=None):
        """Establish a client connection to a server.

        [component only]

        :Parameters:
            - `server`: name or address of the server to use.  If not given
              then use the one specified when creating the object.
            - `port`: port number of the server to use.  If not given then use
              the one specified when creating the object.

        :Types:
            - `server`: `unicode`
            - `port`: `int`"""
        self.lock.acquire()
        try:
            self._connect(server,port)
        finally:
            self.lock.release()