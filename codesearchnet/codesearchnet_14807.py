def start_api_and_rpc_workers(self):
        """Initializes eventlet and starts wait for workers to exit.

        Spawns the workers returned from serve_rpc
        """
        pool = eventlet.GreenPool()

        quark_rpc = self.serve_rpc()
        pool.spawn(quark_rpc.wait)

        pool.waitall()