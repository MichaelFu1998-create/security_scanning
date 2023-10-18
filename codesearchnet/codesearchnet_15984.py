def call(self, call_params):
        """REST Call Helper
        """
        path = '/' + self.api_version + '/Call/'
        method = 'POST'
        return self.request(path, method, call_params)