def run_elective(self, cmd, *args, **kwargs):
        """Run a command, or just echo it, depending on `commit`."""
        if self._commit:
            return self.run(cmd, *args, **kwargs)
        else:
            notify.warning("WOULD RUN: {}".format(cmd))
            kwargs = kwargs.copy()
            kwargs['echo'] = False
            return self.run('true', *args, **kwargs)