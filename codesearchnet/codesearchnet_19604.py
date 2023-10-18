def modulename(cls, depth=1):
        """
        get caller's __name__
        """
        depth += cls.extra_depth
        frame = sys._getframe(depth)
        return frame.f_globals['__name__']