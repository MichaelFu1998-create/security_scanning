def delete_shifts(self, shifts):
        """
        Delete existing shifts.

        http://dev.wheniwork.com/#delete-shift
        """
        url = "/2/shifts/?%s" % urlencode(
            {'ids': ",".join(str(s) for s in shifts)})

        data = self._delete_resource(url)

        return data