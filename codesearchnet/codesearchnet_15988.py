def hangup_all_calls(self):
        """REST Hangup All Live Calls Helper
        """
        path = '/' + self.api_version + '/HangupAllCalls/'
        method = 'POST'
        return self.request(path, method)