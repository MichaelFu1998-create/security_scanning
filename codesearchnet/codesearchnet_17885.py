def query_invitations(cls, user, eager=False):
        """Get all invitations for given user."""
        if eager:
            eager = [Membership.group]
        return cls.query_by_user(user, state=MembershipState.PENDING_USER,
                                 eager=eager)