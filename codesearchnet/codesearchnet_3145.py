def pop_record_writes(self):
        """
        Stop recording trace and return a `list[(address, value)]` of all the writes
        that occurred, where `value` is of type list[str]. Can be called without
        intermediate `pop_record_writes()`.

        For example::

            mem.push_record_writes()
                mem.write(1, 'a')
                mem.push_record_writes()
                    mem.write(2, 'b')
                mem.pop_record_writes()  # Will return [(2, 'b')]
            mem.pop_record_writes()  # Will return [(1, 'a'), (2, 'b')]

        Multiple writes to the same address will all be included in the trace in the
        same order they occurred.

        :return: list[tuple]
        """

        lst = self._recording_stack.pop()
        # Append the current list to a previously-started trace.
        if self._recording_stack:
            self._recording_stack[-1].extend(lst)
        return lst