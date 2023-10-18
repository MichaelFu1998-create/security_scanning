def validate(cls, policy):
        """Validate subscription policy value."""
        return policy in [cls.OPEN, cls.APPROVAL, cls.CLOSED]