def cancel_scheduled_play(self, call_params):
        """REST Cancel a Scheduled Play Helper
        """
        path = '/' + self.api_version + '/CancelScheduledPlay/'
        method = 'POST'
        return self.request(path, method, call_params)