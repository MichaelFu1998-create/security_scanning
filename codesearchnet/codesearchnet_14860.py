def start_rpc_listeners(self):
        """Configure all listeners here"""
        self._setup_rpc()
        if not self.endpoints:
            return []
        self.conn = n_rpc.create_connection()
        self.conn.create_consumer(self.topic, self.endpoints,
                                  fanout=False)
        return self.conn.consume_in_threads()