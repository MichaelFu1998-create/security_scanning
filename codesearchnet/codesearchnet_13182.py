def refresh(self):
        """(a)sync refresh the data."""
        if self.client.is_async:
            return self._arefresh()
        data, cached, ts, response = self.client._request(self.response.url, timeout=None, refresh=True)
        return self.from_data(data, cached, ts, response)