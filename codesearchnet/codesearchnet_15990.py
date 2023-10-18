def schedule_hangup(self, call_params):
        """REST Schedule Hangup Helper
        """
        path = '/' + self.api_version + '/ScheduleHangup/'
        method = 'POST'
        return self.request(path, method, call_params)