def create(cls, group, admin):
        """Create a new group admin.

        :param group: Group object.
        :param admin: Admin object.
        :returns: Newly created GroupAdmin object.
        :raises: IntegrityError
        """
        with db.session.begin_nested():
            obj = cls(
                group=group,
                admin=admin,
            )
            db.session.add(obj)
        return obj