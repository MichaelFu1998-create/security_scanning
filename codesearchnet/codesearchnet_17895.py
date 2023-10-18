def delete(cls, group, admin):
        """Delete admin from group.

        :param group: Group object.
        :param admin: Admin object.
        """
        with db.session.begin_nested():
            obj = cls.query.filter(
                cls.admin == admin, cls.group == group).one()
            db.session.delete(obj)