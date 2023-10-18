def _flann_args(self, X=None):
        "The dictionary of arguments to give to FLANN."
        args = {'cores': self._n_jobs}
        if self.flann_algorithm == 'auto':
            if X is None or X.dim > 5:
                args['algorithm'] = 'linear'
            else:
                args['algorithm'] = 'kdtree_single'
        else:
            args['algorithm'] = self.flann_algorithm
        if self.flann_args:
            args.update(self.flann_args)

        # check that arguments are correct
        try:
            FLANNParameters().update(args)
        except AttributeError as e:
            msg = "flann_args contains an invalid argument:\n  {}"
            raise TypeError(msg.format(e))

        return args