def suggest(self, history, searchspace):
        """
        Suggest params to maximize an objective function based on the
        function evaluation history using a tree of Parzen estimators (TPE),
        as implemented in the hyperopt package.

        Use of this function requires that hyperopt be installed.
        """
        # This function is very odd, because as far as I can tell there's
        # no real documented API for any of the internals of hyperopt. Its
        # execution model is that hyperopt calls your objective function
        # (instead of merely providing you with suggested points, and then
        # you calling the function yourself), and its very tricky (for me)
        # to use the internal hyperopt data structures to get these predictions
        # out directly.

        # so they path we take in this function is to construct a synthetic
        # hyperopt.Trials database which from the `history`, and then call
        # hyoperopt.fmin with a dummy objective function that logs the value
        # used, and then return that value to our client.

        # The form of the hyperopt.Trials database isn't really documented in
        # the code -- most of this comes from reverse engineering it, by
        # running fmin() on a simple function and then inspecting the form of
        # the resulting trials object.
        if 'hyperopt' not in sys.modules:
            raise ImportError('No module named hyperopt')

        random = check_random_state(self.seed)
        hp_searchspace = searchspace.to_hyperopt()

        trials = Trials()
        for i, (params, scores, status) in enumerate(history):
            if status == 'SUCCEEDED':
                # we're doing maximization, hyperopt.fmin() does minimization,
                # so we need to swap the sign
                result = {'loss': -np.mean(scores), 'status': STATUS_OK}
            elif status == 'PENDING':
                result = {'status': STATUS_RUNNING}
            elif status == 'FAILED':
                result = {'status': STATUS_FAIL}
            else:
                raise RuntimeError('unrecognized status: %s' % status)

            # the vals key in the trials dict is basically just the params
            # dict, but enum variables (hyperopt hp.choice() nodes) are
            # different, because the index of the parameter is specified
            # in vals, not the parameter itself.

            vals = {}
            for var in searchspace:
                if isinstance(var, EnumVariable):
                    # get the index in the choices of the parameter, and use
                    # that.
                    matches = [
                        i for i, c in enumerate(var.choices)
                        if c == params[var.name]
                    ]
                    assert len(matches) == 1
                    vals[var.name] = matches
                else:
                    # the other big difference is that all of the param values
                    # are wrapped in length-1 lists.
                    vals[var.name] = [params[var.name]]

            trials.insert_trial_doc({
                'misc': {
                    'cmd': ('domain_attachment', 'FMinIter_Domain'),
                    'idxs': dict((k, [i]) for k in hp_searchspace.keys()),
                    'tid': i,
                    'vals': vals,
                    'workdir': None
                },
                'result': result,
                'tid': i,
                # bunch of fixed fields that hyperopt seems to require
                'owner': None,
                'spec': None,
                'state': 2,
                'book_time': None,
                'exp_key': None,
                'refresh_time': None,
                'version': 0
            })

        trials.refresh()
        chosen_params_container = []

        def suggest(*args, **kwargs):
            return tpe.suggest(*args,
                               **kwargs,
                               gamma=self.gamma,
                               n_startup_jobs=self.seeds)

        def mock_fn(x):
            # http://stackoverflow.com/a/3190783/1079728
            # to get around no nonlocal keywork in python2
            chosen_params_container.append(x)
            return 0

        fmin(fn=mock_fn,
             algo=tpe.suggest,
             space=hp_searchspace,
             trials=trials,
             max_evals=len(trials.trials) + 1,
             **self._hyperopt_fmin_random_kwarg(random))
        chosen_params = chosen_params_container[0]

        return chosen_params