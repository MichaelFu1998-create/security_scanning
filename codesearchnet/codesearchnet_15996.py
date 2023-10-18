def play_stop(self, call_params):
        """REST PlayStop on a Call Helper
        """
        path = '/' + self.api_version + '/PlayStop/'
        method = 'POST'
        return self.request(path, method, call_params)