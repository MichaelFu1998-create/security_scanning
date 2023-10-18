def connect(self, node="", rpcuser="", rpcpassword="", **kwargs):
        """ Connect to blockchain network (internal use only)
        """
        if not node:
            if "node" in self.config:
                node = self.config["node"]
            else:
                raise ValueError("A Blockchain node needs to be provided!")

        if not rpcuser and "rpcuser" in self.config:
            rpcuser = self.config["rpcuser"]

        if not rpcpassword and "rpcpassword" in self.config:
            rpcpassword = self.config["rpcpassword"]

        self.rpc = self.rpc_class(node, rpcuser, rpcpassword, **kwargs)