def delete(cls, group, user):
        """Delete membership."""
        with db.session.begin_nested():
            cls.query.filter_by(group=group, user_id=user.get_id()).delete()