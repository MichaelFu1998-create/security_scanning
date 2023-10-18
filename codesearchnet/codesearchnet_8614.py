def update_throttle_scope(self):
        """
        Update throttle scope so that service user throttle rates are applied.
        """
        self.scope = SERVICE_USER_SCOPE
        self.rate = self.get_rate()
        self.num_requests, self.duration = self.parse_rate(self.rate)