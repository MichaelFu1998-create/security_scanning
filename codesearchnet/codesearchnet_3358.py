def _solver_version(self) -> Version:
        """
        If we fail to parse the version, we assume z3's output has changed, meaning it's a newer
        version than what's used now, and therefore ok.

        Anticipated version_cmd_output format: 'Z3 version 4.4.2'
                                               'Z3 version 4.4.5 - 64 bit - build hashcode $Z3GITHASH'
        """
        self._reset()
        if self._received_version is None:
            self._send('(get-info :version)')
            self._received_version = self._recv()
        key, version = shlex.split(self._received_version[1:-1])
        return Version(*map(int, version.split('.')))