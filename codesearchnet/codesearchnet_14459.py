def estimator(self):
        """Get the estimator, an instance of a (subclass of)
        sklearn.base.BaseEstimator

        It can be loaded either from a pickle, from a string using eval(),
        or from an entry point.

        e.g.

        estimator:
            # only one of the following can actually be active in a given
            # config file.
            pickle: path-to-pickle-file.pkl
            eval: "Pipeline([('cluster': KMeans())])"
            entry_point: sklearn.linear_model.LogisticRegression
            module: myestimator
        """
        module_path = self.get_value('estimator/module')
        if module_path is not None:
            with prepend_syspath(dirname(abspath(self.path))):
                estimator_module = importlib.import_module(module_path)
            estimator = estimator_module.estimator()
            if not isinstance(estimator, sklearn.base.BaseEstimator):
                raise RuntimeError('estimator/pickle must load a '
                                   'sklearn-derived Estimator')
            return estimator

        evalstring = self.get_value('estimator/eval')
        if evalstring is not None:
            got = self.get_value('estimator/eval_scope')
            if isinstance(got, six.string_types):
                got = [got]
            elif isinstance(got, list):
                pass
            else:
                raise RuntimeError('unexpected type for estimator/eval_scope')

            scope = {}
            for pkg_name in got:
                if pkg_name in eval_scopes.__all__:
                    scope.update(getattr(eval_scopes, pkg_name)())
                else:
                    try:
                        pkg = importlib.import_module(pkg_name)
                    except ImportError as e:
                        raise RuntimeError(str(e))
                    scope.update(eval_scopes.import_all_estimators(pkg))

            try:
                estimator = eval(evalstring, {}, scope)
                if not isinstance(estimator, sklearn.base.BaseEstimator):
                    raise RuntimeError('estimator/pickle must load a '
                                       'sklearn-derived Estimator')
                return estimator
            except:
                print('-'*78, file=sys.stderr)
                print('Error parsing estimator/eval', file=sys.stderr)
                print('-'*78, file=sys.stderr)

                traceback.print_exc(file=sys.stderr)
                print('-'*78, file=sys.stderr)
                sys.exit(1)

        entry_point = self.get_value('estimator/entry_point')
        if entry_point is not None:
            estimator = load_entry_point(entry_point, 'estimator/entry_point')
            if issubclass(estimator, sklearn.base.BaseEstimator):
                estimator = estimator(
                    **self.get_value('estimator/params', default={}))
            if not isinstance(estimator, sklearn.base.BaseEstimator):
                raise RuntimeError('estimator/pickle must load a '
                                   'sklearn-derived Estimator')
            return estimator

        # load estimator from pickle field
        pkl = self.get_value('estimator/pickle')
        if pkl is not None:
            pickl_dir = dirname(abspath(self.path))
            path = join(pickl_dir, pkl)
            if not isfile(path):
                raise RuntimeError('estimator/pickle %s is not a file' % pkl)
            with open(path, 'rb') as f:
                with prepend_syspath(pickl_dir):
                    estimator = cPickle.load(f)
                if not isinstance(estimator, sklearn.base.BaseEstimator):
                    raise RuntimeError('estimator/pickle must load a '
                                       'sklearn-derived Estimator')
                return estimator

        raise RuntimeError('no estimator field')