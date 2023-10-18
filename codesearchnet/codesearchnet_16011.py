def conference_list(self, call_params):
        """REST Conference List Helper
        """
        path = '/' + self.api_version + '/ConferenceList/'
        method = 'POST'
        return self.request(path, method, call_params)