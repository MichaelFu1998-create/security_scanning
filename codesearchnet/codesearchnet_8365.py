def rpcexec(self, payload):
        """ Execute a call by sending the payload

            :param json payload: Payload data
            :raises ValueError: if the server does not respond in proper JSON
                format
        """
        if not self.ws:  # pragma: no cover
            self.connect()

        log.debug(json.dumps(payload))

        # Mutex/Lock
        # We need to lock because we need to wait for websocket
        # response but don't want to allow other threads to send
        # requests (that might take less time) to disturb
        self.__lock.acquire()

        # Send over websocket
        try:
            self.ws.send(json.dumps(payload, ensure_ascii=False).encode("utf8"))
            # Receive from websocket
            ret = self.ws.recv()

        finally:
            # Release lock
            self.__lock.release()

        return ret