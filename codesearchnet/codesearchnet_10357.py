def commandline(self, *args, **kwargs):
        """Returns the commandline that run() uses (without pipes)."""
        # this mirrors the setup in run()
        _args, _kwargs = self._combine_arglist(args, kwargs)
        return self._commandline(*_args, **_kwargs)