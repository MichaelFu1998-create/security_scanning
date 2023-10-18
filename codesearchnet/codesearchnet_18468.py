def is_ambiguous(self, dt, idx=None):
        """
        Whether or not the "wall time" of a given datetime is ambiguous in this
        zone.

        :param dt:
            A :py:class:`datetime.datetime`, naive or time zone aware.


        :return:
            Returns ``True`` if ambiguous, ``False`` otherwise.

        .. versionadded:: 2.6.0
        """
        if idx is None:
            idx = self._find_last_transition(dt)

        # Calculate the difference in offsets from current to previous
        timestamp = _datetime_to_timestamp(dt)
        tti = self._get_ttinfo(idx)

        if idx is None or idx <= 0:
            return False

        od = self._get_ttinfo(idx - 1).offset - tti.offset
        tt = self._trans_list[idx]          # Transition time

        return timestamp < tt + od