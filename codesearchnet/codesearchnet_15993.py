def record_stop(self, call_params):
        """REST RecordStop
        """
        path = '/' + self.api_version + '/RecordStop/'
        method = 'POST'
        return self.request(path, method, call_params)