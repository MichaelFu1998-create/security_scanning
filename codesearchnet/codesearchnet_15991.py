def cancel_scheduled_hangup(self, call_params):
        """REST Cancel a Scheduled Hangup Helper
        """
        path = '/' + self.api_version + '/CancelScheduledHangup/'
        method = 'POST'
        return self.request(path, method, call_params)