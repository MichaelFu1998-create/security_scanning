def check(self, mark=0, err_msg="", **kwds):
        """
        :param mark:
            0 - do not need check return value or error()
            1 - check error()
            2 - check return value
        """
        unexpected_ret = kwds.get("unexpected_ret", (0,))

        def _check(fn):
            @wraps(fn)
            def wrapper(*args, **kwargs):
                ret = fn(*args, **kwargs)

                flags = reduce(
                    self._parser, [dict(num=mark, flags=[]), 2, 1])["flags"]

                if 1 in flags:
                    if self._has_error():
                        raise AutoItError(err_msg)

                if 2 in flags:
                    if self._has_unexpected_ret(ret, unexpected_ret):
                        raise AutoItError(err_msg)

                return ret
            return wrapper
        return _check