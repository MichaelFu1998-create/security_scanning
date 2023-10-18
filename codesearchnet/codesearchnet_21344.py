def make_cache_keys(self, endpoint, kwargs):
        """ This function is built to provide cache keys for templates

        :param endpoint: Current endpoint
        :param kwargs: Keyword Arguments
        :return: tuple of i18n dependant cache key and i18n ignoring cache key
        :rtype: tuple(str)
        """
        keys = sorted(kwargs.keys())
        i18n_cache_key = endpoint+"|"+"|".join([kwargs[k] for k in keys])
        if "lang" in keys:
            cache_key = endpoint+"|" + "|".join([kwargs[k] for k in keys if k != "lang"])
        else:
            cache_key = i18n_cache_key
        return i18n_cache_key, cache_key