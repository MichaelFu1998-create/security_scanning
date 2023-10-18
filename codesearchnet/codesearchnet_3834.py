def ensure(self, func, *args, **kwargs):
        r"""
        Wraps around a function. A cfgstr must be stored in the base cacher.

        Args:
            func (callable): function that will compute data on cache miss
            *args: passed to func
            **kwargs: passed to func

        Example:
            >>> from ubelt.util_cache import *  # NOQA
            >>> def func():
            >>>     return 'expensive result'
            >>> fname = 'test_cacher_ensure'
            >>> cfgstr = 'func params'
            >>> cacher = Cacher(fname, cfgstr)
            >>> cacher.clear()
            >>> data1 = cacher.ensure(func)
            >>> data2 = cacher.ensure(func)
            >>> assert data1 == 'expensive result'
            >>> assert data1 == data2
            >>> cacher.clear()
        """
        data = self.tryload()
        if data is None:
            data = func(*args, **kwargs)
            self.save(data)
        return data