def _rc_brpoplpush(self, src, dst, timeout=0):
        """
        Pop a value off the tail of ``src``, push it on the head of ``dst``
        and then return it.

        This command blocks until a value is in ``src`` or until ``timeout``
        seconds elapse, whichever is first. A ``timeout`` value of 0 blocks
        forever.
        Not atomic
        """
        rpop = self.brpop(src, timeout)
        if rpop is not None:
            self.lpush(dst, rpop[1])
            return rpop[1]
        return None