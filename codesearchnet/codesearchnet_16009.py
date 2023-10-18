def conference_play(self, call_params):
        """REST Conference Play helper
        """
        path = '/' + self.api_version + '/ConferencePlay/'
        method = 'POST'
        return self.request(path, method, call_params)