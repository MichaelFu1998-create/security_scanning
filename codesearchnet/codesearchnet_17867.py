def validate(cls, state):
        """Validate state value."""
        return state in [cls.ACTIVE, cls.PENDING_ADMIN, cls.PENDING_USER]