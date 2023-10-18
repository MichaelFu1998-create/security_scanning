def conference_speak(self, call_params):
        """REST Conference Speak helper
        """
        path = '/' + self.api_version + '/ConferenceSpeak/'
        method = 'POST'
        return self.request(path, method, call_params)