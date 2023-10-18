def conference_kick(self, call_params):
        """REST Conference Kick helper
        """
        path = '/' + self.api_version + '/ConferenceKick/'
        method = 'POST'
        return self.request(path, method, call_params)