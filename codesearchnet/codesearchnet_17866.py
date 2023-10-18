def validate(cls, policy):
        """Validate privacy policy value."""
        return policy in [cls.PUBLIC, cls.MEMBERS, cls.ADMINS]