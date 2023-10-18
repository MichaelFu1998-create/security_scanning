def hangup_call(self, call_params):
        """REST Hangup Live Call Helper
        """
        path = '/' + self.api_version + '/HangupCall/'
        method = 'POST'
        return self.request(path, method, call_params)