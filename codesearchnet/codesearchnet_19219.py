def format_seconds(self, n_seconds):
        """Format a time in seconds."""
        func = self.ok
        if n_seconds >= 60:
            n_minutes, n_seconds = divmod(n_seconds, 60)
            return "%s minutes %s seconds" % (
                        func("%d" % n_minutes),
                        func("%.3f" % n_seconds))
        else:
            return "%s seconds" % (
                        func("%.3f" % n_seconds))