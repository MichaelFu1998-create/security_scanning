def query_by_user(cls, user, **kwargs):
        """Get a user's memberships."""
        return cls._filter(
            cls.query.filter_by(user_id=user.get_id()),
            **kwargs
        )