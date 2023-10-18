def reload_cache_config(self, call_params):
        """REST Reload Plivo Cache Config helper
        """
        path = '/' + self.api_version + '/ReloadCacheConfig/'
        method = 'POST'
        return self.request(path, method, call_params)