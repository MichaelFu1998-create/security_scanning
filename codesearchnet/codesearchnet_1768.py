def randrange(self, start, stop=None, step=1, _int=int, _maxwidth=1L<<BPF):
        """Choose a random item from range(start, stop[, step]).

        This fixes the problem with randint() which includes the
        endpoint; in Python this is usually not what you want.

        """

        # This code is a bit messy to make it fast for the
        # common case while still doing adequate error checking.
        istart = _int(start)
        if istart != start:
            raise ValueError, "non-integer arg 1 for randrange()"
        if stop is None:
            if istart > 0:
                if istart >= _maxwidth:
                    return self._randbelow(istart)
                return _int(self.random() * istart)
            raise ValueError, "empty range for randrange()"

        # stop argument supplied.
        istop = _int(stop)
        if istop != stop:
            raise ValueError, "non-integer stop for randrange()"
        width = istop - istart
        if step == 1 and width > 0:
            # Note that
            #     int(istart + self.random()*width)
            # instead would be incorrect.  For example, consider istart
            # = -2 and istop = 0.  Then the guts would be in
            # -2.0 to 0.0 exclusive on both ends (ignoring that random()
            # might return 0.0), and because int() truncates toward 0, the
            # final result would be -1 or 0 (instead of -2 or -1).
            #     istart + int(self.random()*width)
            # would also be incorrect, for a subtler reason:  the RHS
            # can return a long, and then randrange() would also return
            # a long, but we're supposed to return an int (for backward
            # compatibility).

            if width >= _maxwidth:
                return _int(istart + self._randbelow(width))
            return _int(istart + _int(self.random()*width))
        if step == 1:
            raise ValueError, "empty range for randrange() (%d,%d, %d)" % (istart, istop, width)

        # Non-unit step argument supplied.
        istep = _int(step)
        if istep != step:
            raise ValueError, "non-integer step for randrange()"
        if istep > 0:
            n = (width + istep - 1) // istep
        elif istep < 0:
            n = (width + istep + 1) // istep
        else:
            raise ValueError, "zero step for randrange()"

        if n <= 0:
            raise ValueError, "empty range for randrange()"

        if n >= _maxwidth:
            return istart + istep*self._randbelow(n)
        return istart + istep*_int(self.random() * n)