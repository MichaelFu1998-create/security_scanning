def get_by_name(cls, name):
        """Query group by a group name.

        :param name: Name of a group to search for.
        :returns: Group object or None.
        """
        try:
            return cls.query.filter_by(name=name).one()
        except NoResultFound:
            return None