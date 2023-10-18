def create_shift(self, params={}):
        """
        Creates a shift

        http://dev.wheniwork.com/#create/update-shift
        """
        url = "/2/shifts/"
        body = params

        data = self._post_resource(url, body)
        shift = self.shift_from_json(data["shift"])

        return shift