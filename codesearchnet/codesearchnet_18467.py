def fromutc(self, dt):
        """
        The ``tzfile`` implementation of :py:func:`datetime.tzinfo.fromutc`.

        :param dt:
            A :py:class:`datetime.datetime` object.

        :raises TypeError:
            Raised if ``dt`` is not a :py:class:`datetime.datetime` object.

        :raises ValueError:
            Raised if this is called with a ``dt`` which does not have this
            ``tzinfo`` attached.

        :return:
            Returns a :py:class:`datetime.datetime` object representing the
            wall time in ``self``'s time zone.
        """
        # These isinstance checks are in datetime.tzinfo, so we'll preserve
        # them, even if we don't care about duck typing.
        if not isinstance(dt, datetime.datetime):
            raise TypeError("fromutc() requires a datetime argument")

        if dt.tzinfo is not self:
            raise ValueError("dt.tzinfo is not self")

        # First treat UTC as wall time and get the transition we're in.
        idx = self._find_last_transition(dt, in_utc=True)
        tti = self._get_ttinfo(idx)

        dt_out = dt + datetime.timedelta(seconds=tti.offset)

        fold = self.is_ambiguous(dt_out, idx=idx)

        return enfold(dt_out, fold=int(fold))