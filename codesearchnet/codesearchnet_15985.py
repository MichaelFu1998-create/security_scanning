def bulk_call(self, call_params):
        """REST BulkCalls Helper
        """
        path = '/' + self.api_version + '/BulkCall/'
        method = 'POST'
        return self.request(path, method, call_params)