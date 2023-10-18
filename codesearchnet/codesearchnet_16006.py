def conference_undeaf(self, call_params):
        """REST Conference Undeaf helper
        """
        path = '/' + self.api_version + '/ConferenceUndeaf/'
        method = 'POST'
        return self.request(path, method, call_params)