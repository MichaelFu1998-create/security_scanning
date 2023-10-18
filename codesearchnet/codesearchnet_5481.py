def insert_rule(self, chain, src=None, dest=None, target=None):
        """Insert a new rule in the chain
        """
        if not chain:
            raise ValueError("Invalid chain")
        if not target:
            raise ValueError("Invalid target")
        if not (src or dest):
            raise ValueError("Need src, dest, or both")

        args = ["-I", chain]
        if src:
            args += ["-s", src]
        if dest:
            args += ["-d", dest]
        args += ["-j", target]
        self.call(*args)