def get_log(self, log_id, timeout=None):
        """ API call to get a specific log entry """
        return self._api_request(
            self.GET_LOG_ENDPOINT % log_id,
            self.HTTP_GET,
            timeout=timeout
        )