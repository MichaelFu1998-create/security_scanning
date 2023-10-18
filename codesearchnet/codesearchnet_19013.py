def _rc_rpoplpush(self, src, dst):
        """
        RPOP a value off of the ``src`` list and LPUSH it
        on to the ``dst`` list.  Returns the value.
        """
        rpop = self.rpop(src)
        if rpop is not None:
            self.lpush(dst, rpop)
            return rpop
        return None