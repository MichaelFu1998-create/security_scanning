def gradient_optimizer(coro):
    """Turns a coroutine into a gradient based optimizer."""

    class GradientOptimizer(Optimizer):

        @wraps(coro)
        def __init__(self, *args, **kwargs):
            self.algorithm = coro(*args, **kwargs)
            self.algorithm.send(None)
            self.operators = []

        def set_transform(self, func):
            self.transform = compose(destruct, func, self.restruct)

        def minimize(self, f_df, x0, display=sys.stdout, maxiter=1e3):

            self.display = display
            self.theta = x0

            # setup
            xk = self.algorithm.send(destruct(x0).copy())
            store = defaultdict(list)
            runtimes = []
            if len(self.operators) == 0:
                self.operators = [proxops.identity()]

            # setup
            obj, grad = wrap(f_df, x0)
            transform = compose(destruct, *reversed(self.operators), self.restruct)

            self.optional_print(tp.header(['Iteration', 'Objective', '||Grad||', 'Runtime']))
            try:
                for k in count():

                    # setup
                    tstart = perf_counter()
                    f = obj(xk)
                    df = grad(xk)
                    xk = transform(self.algorithm.send(df))
                    runtimes.append(perf_counter() - tstart)
                    store['f'].append(f)

                    # Update display
                    self.optional_print(tp.row([k,
                                                f,
                                                np.linalg.norm(destruct(df)),
                                                tp.humantime(runtimes[-1])]))

                    if k >= maxiter:
                        break

            except KeyboardInterrupt:
                pass

            self.optional_print(tp.bottom(4))

            # cleanup
            self.optional_print(u'\u279b Final objective: {}'.format(store['f'][-1]))
            self.optional_print(u'\u279b Total runtime: {}'.format(tp.humantime(sum(runtimes))))
            self.optional_print(u'\u279b Per iteration runtime: {} +/- {}'.format(
                tp.humantime(np.mean(runtimes)),
                tp.humantime(np.std(runtimes)),
            ))

            # result
            return OptimizeResult({
                'x': self.restruct(xk),
                'f': f,
                'df': self.restruct(df),
                'k': k,
                'obj': np.array(store['f']),
            })

    return GradientOptimizer