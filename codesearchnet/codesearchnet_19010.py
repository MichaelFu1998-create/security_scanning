def getnodefor(self, name):
        "Return the node where the ``name`` would land to"
        node = self._getnodenamefor(name)
        return {node: self.cluster['nodes'][node]}