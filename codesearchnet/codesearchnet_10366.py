def transform_args(self,*args,**kwargs):
        """Combine arguments and turn them into gromacs tool arguments."""
        newargs = self._combineargs(*args, **kwargs)
        return self._build_arg_list(**newargs)