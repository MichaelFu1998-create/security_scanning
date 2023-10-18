def update_lazyevals(self):
        """Update all LazyEvals in self

        self.lzy_evals must be set to LazyEval object(s) enough to
        update all owned LazyEval objects.
        """
        if self.lazy_evals is None:
            return
        elif isinstance(self.lazy_evals, LazyEval):
            self.lazy_evals.get_updated()
        else:
            for lz in self.lazy_evals:
                lz.get_updated()