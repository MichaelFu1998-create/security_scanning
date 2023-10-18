def conference_hangup(self, call_params):
        """REST Conference Hangup helper
        """
        path = '/' + self.api_version + '/ConferenceHangup/'
        method = 'POST'
        return self.request(path, method, call_params)