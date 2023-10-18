def play(self, call_params):
        """REST Play something on a Call Helper
        """
        path = '/' + self.api_version + '/Play/'
        method = 'POST'
        return self.request(path, method, call_params)