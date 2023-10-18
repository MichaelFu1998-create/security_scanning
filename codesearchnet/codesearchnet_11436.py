def set_search_enviroment(cls, **kwargs):
        """
        Called from within search handler
        Finds desired subclass and calls initialize method
        """
        initializer = _load_class(getattr(settings, "SEARCH_INITIALIZER", None), cls)()
        return initializer.initialize(**kwargs)