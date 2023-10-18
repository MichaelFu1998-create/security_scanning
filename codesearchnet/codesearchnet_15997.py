def schedule_play(self, call_params):
        """REST Schedule playing something on a call Helper
        """
        path = '/' + self.api_version + '/SchedulePlay/'
        method = 'POST'
        return self.request(path, method, call_params)