def MetaOrdered(parallel, done, turnstile):
    """meta class for Ordered construct."""
    class Ordered:
        def __init__(self, iterref):
            if parallel.master:
                done[...] = 0
            self.iterref = iterref
            parallel.barrier()

        @classmethod
        def abort(self):
            turnstile.release()

        def __enter__(self):
            while self.iterref != done:
                pass
            turnstile.acquire()
            return self
        def __exit__(self, *args):
            done[...] += 1
            turnstile.release()
    return Ordered