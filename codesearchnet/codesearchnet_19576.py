def push_job(self, fun, *args, **kwargs):
        """
        put job if possible, non-blocking
        :param fun:
        :param args:
        :param kwargs:
        :return:
        """
        assert callable(fun)
        return self.put((fun, args, kwargs), block=True)