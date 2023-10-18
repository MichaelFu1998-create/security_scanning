def group_call(self, call_params):
        """REST GroupCalls Helper
        """
        path = '/' + self.api_version + '/GroupCall/'
        method = 'POST'
        return self.request(path, method, call_params)