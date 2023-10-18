def pid(self):
        """Return an instance of deposit PID."""
        pid = self.deposit_fetcher(self.id, self)
        return PersistentIdentifier.get(pid.pid_type,
                                        pid.pid_value)