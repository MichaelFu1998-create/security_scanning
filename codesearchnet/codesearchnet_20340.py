def list(self, url_components=()):
        """
        Send list request for all members of a collection
        """
        resp = self.get(url_components)
        return resp.get(self.result_key, [])