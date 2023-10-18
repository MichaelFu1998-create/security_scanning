def conference_list_members(self, call_params):
        """REST Conference List Members Helper
        """
        path = '/' + self.api_version + '/ConferenceListMembers/'
        method = 'POST'
        return self.request(path, method, call_params)