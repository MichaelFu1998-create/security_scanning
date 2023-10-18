def _json(self, response, status_code):
        """Extract JSON from response if `status_code` matches."""
        if isinstance(status_code, numbers.Integral):
            status_code = (status_code,)

        if response.status_code in status_code:
            return response.json()
        else:
            raise RuntimeError("Response has status "
                               "code {} not {}".format(response.status_code,
                                                       status_code))