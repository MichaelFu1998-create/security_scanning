def transfer_call(self, call_params):
        """REST Transfer Live Call Helper
        """
        path = '/' + self.api_version + '/TransferCall/'
        method = 'POST'
        return self.request(path, method, call_params)