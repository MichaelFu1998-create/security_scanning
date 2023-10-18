def put_job(self, fun, *args, **kwargs):
        """
        put job if possible, non-blocking
        :param fun:
        :param args:
        :param kwargs:
        :return:
        """
        if not args and not kwargs and isinstance(fun, (tuple, list)):
            # ex) q.put_job([fun, args, kwargs])
            fun, args, kwargs = fun

        assert callable(fun)
        return self.put((fun, args, kwargs), block=False)