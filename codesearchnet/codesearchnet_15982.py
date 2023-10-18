def reload_config(self, call_params):
        """REST Reload Plivo Config helper
        """
        path = '/' + self.api_version + '/ReloadConfig/'
        method = 'POST'
        return self.request(path, method, call_params)