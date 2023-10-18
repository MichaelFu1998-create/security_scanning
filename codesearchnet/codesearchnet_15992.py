def record_start(self, call_params):
        """REST RecordStart helper
        """
        path = '/' + self.api_version + '/RecordStart/'
        method = 'POST'
        return self.request(path, method, call_params)