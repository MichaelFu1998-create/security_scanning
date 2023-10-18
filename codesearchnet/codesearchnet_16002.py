def conference_unmute(self, call_params):
        """REST Conference Unmute helper
        """
        path = '/' + self.api_version + '/ConferenceUnmute/'
        method = 'POST'
        return self.request(path, method, call_params)