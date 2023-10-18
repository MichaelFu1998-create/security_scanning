def _spawn_heartbeat(self):
        """This functions returns a list of jobs"""
        self.spawn(self._heartbeat)
        self.spawn(self._heartbeat_timeout)