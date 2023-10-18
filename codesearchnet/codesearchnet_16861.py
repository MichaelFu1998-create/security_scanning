def get_log_events(self, log_id, timeout=None):
        """ API call to get a specific log entry """
        return self._api_request(
            self.GET_LOG_EVENTS_ENDPOINT % log_id,
            self.HTTP_GET,
            timeout=timeout
        )