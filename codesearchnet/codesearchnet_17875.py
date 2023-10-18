def add_member(self, user, state=MembershipState.ACTIVE):
        """Invite a user to a group.

        :param user: User to be added as a group member.
        :param state: MembershipState. Default: MembershipState.ACTIVE.
        :returns: Membership object or None.
        """
        return Membership.create(self, user, state)