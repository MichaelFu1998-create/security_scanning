def get(cls, group, user):
        """Get membership for given user and group.

        :param group: Group object.
        :param user: User object.
        :returns: Membership or None.
        """
        try:
            m = cls.query.filter_by(user_id=user.get_id(), group=group).one()
            return m
        except Exception:
            return None