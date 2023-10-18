def conference_mute(self, call_params):
        """REST Conference Mute helper
        """
        path = '/' + self.api_version + '/ConferenceMute/'
        method = 'POST'
        return self.request(path, method, call_params)