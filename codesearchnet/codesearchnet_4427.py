def _add_input_deps(self, executor, args, kwargs):
        """Look for inputs of the app that are remote files. Submit stage_in
        apps for such files and replace the file objects in the inputs list with
        corresponding DataFuture objects.

        Args:
            - executor (str) : executor where the app is going to be launched
            - args (List) : Positional args to app function
            - kwargs (Dict) : Kwargs to app function
        """

        # Return if the task is _*_stage_in
        if executor == 'data_manager':
            return args, kwargs

        inputs = kwargs.get('inputs', [])
        for idx, f in enumerate(inputs):
            if isinstance(f, File) and f.is_remote():
                inputs[idx] = self.data_manager.stage_in(f, executor)

        for kwarg, f in kwargs.items():
            if isinstance(f, File) and f.is_remote():
                kwargs[kwarg] = self.data_manager.stage_in(f, executor)

        newargs = list(args)
        for idx, f in enumerate(newargs):
            if isinstance(f, File) and f.is_remote():
                newargs[idx] = self.data_manager.stage_in(f, executor)

        return tuple(newargs), kwargs