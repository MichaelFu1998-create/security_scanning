def _fmt_args_kwargs(self, *some_args, **some_kwargs):
        """Helper to convert the given args and kwargs into a string."""
        if some_args:
            out_args = str(some_args).lstrip('(').rstrip(',)')
        if some_kwargs:
            out_kwargs = ', '.join([str(i).lstrip('(').rstrip(')').replace(', ',': ') for i in [
                    (k,some_kwargs[k]) for k in sorted(some_kwargs.keys())]])

        if some_args and some_kwargs:
            return out_args + ', ' + out_kwargs
        elif some_args:
            return out_args
        elif some_kwargs:
            return out_kwargs
        else:
            return ''