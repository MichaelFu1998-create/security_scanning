def _to_json(self, resp):
        """
            Extract json from a response.
            Assumes response is valid otherwise.
            Internal use only.
        """
        try:
            json = resp.json()
        except ValueError as e:
            reason = "TMC Server did not send valid JSON: {0}"
            raise APIError(reason.format(repr(e)))

        return json