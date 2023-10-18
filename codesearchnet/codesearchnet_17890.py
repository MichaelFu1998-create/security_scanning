def create(cls, group, user, state=MembershipState.ACTIVE):
        """Create a new membership."""
        with db.session.begin_nested():
            membership = cls(
                user_id=user.get_id(),
                id_group=group.id,
                state=state,
            )
            db.session.add(membership)
        return membership