def send_digits(self, call_params):
        """REST Send digits to a Call
        """
        path = '/' + self.api_version + '/SendDigits/'
        method = 'POST'
        return self.request(path, method, call_params)