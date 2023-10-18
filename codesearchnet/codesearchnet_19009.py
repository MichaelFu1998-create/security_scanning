def _getnodenamefor(self, name):
        "Return the node name where the ``name`` would land to"
        return 'node_' + str(
            (abs(binascii.crc32(b(name)) & 0xffffffff) % self.no_servers) + 1)