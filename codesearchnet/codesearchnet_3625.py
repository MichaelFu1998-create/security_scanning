def set_flags(self, **flags):
        """
        Note: For any unmodified flags, update _last_flags with the most recent
        committed value. Otherwise, for example, this could happen:

            overflow=0
            instr1 computes overflow=1, updates _last_flags, doesn't commit
            instr2 updates all flags in _last_flags except overflow (overflow remains 1 in _last_flags)
            instr2 commits all in _last_flags
            now overflow=1 even though it should still be 0
        """
        unupdated_flags = self._last_flags.keys() - flags.keys()
        for flag in unupdated_flags:
            flag_name = f'APSR_{flag}'
            self._last_flags[flag] = self.regfile.read(flag_name)
        self._last_flags.update(flags)