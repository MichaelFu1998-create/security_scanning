def get(self, pk):
        """Return one and exactly one object

        =====API DOCS=====
        Return one and exactly one Tower setting.

        :param pk: Primary key of the Tower setting to retrieve
        :type pk: int
        :returns: loaded JSON of the retrieved Tower setting object.
        :rtype: dict
        :raises tower_cli.exceptions.NotFound: When no specified Tower setting exists.

        =====API DOCS=====
        """
        # The Tower API doesn't provide a mechanism for retrieving a single
        # setting value at a time, so fetch them all and filter
        try:
            return next(s for s in self.list()['results'] if s['id'] == pk)
        except StopIteration:
            raise exc.NotFound('The requested object could not be found.')