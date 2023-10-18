def _rc_smove(self, src, dst, value):
        """
        Move ``value`` from set ``src`` to set ``dst``
        not atomic
        """
        if self.type(src) != b("set"):
            return self.smove(src + "{" + src + "}", dst, value)
        if self.type(dst) != b("set"):
            return self.smove(dst + "{" + dst + "}", src, value)
        if self.srem(src, value):
            return 1 if self.sadd(dst, value) else 0
        return 0