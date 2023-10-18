def conference_deaf(self, call_params):
        """REST Conference Deaf helper
        """
        path = '/' + self.api_version + '/ConferenceDeaf/'
        method = 'POST'
        return self.request(path, method, call_params)