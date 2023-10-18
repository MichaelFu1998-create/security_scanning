def timethis(what):
    """"Utility function for making simple benchmarks (calculates time calls).
    It can be used either as a context manager or as a decorator.
    """
    @contextlib.contextmanager
    def benchmark():
        timer = time.clock if sys.platform == "win32" else time.time
        start = timer()
        yield
        stop = timer()
        res = (stop - start)
        print_bench(what, res, "secs")

    if hasattr(what, "__call__"):
        def timed(*args, **kwargs):
            with benchmark():
                return what(*args, **kwargs)
        return timed
    else:
        return benchmark()