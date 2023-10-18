def run(self, *args, **kwargs):
        """Run the command; args/kwargs are added or replace the ones given to the constructor."""
        _args, _kwargs = self._combine_arglist(args, kwargs)
        results, p = self._run_command(*_args, **_kwargs)
        return results