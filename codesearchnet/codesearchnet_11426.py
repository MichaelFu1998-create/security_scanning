def get_search_engine(index=None):
        """
        Returns the desired implementor (defined in settings)
        """
        search_engine_class = _load_class(getattr(settings, "SEARCH_ENGINE", None), None)
        return search_engine_class(index=index) if search_engine_class else None