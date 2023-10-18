def invite(self, user, admin=None):
        """Invite a user to a group (should be done by admins).

        Wrapper around ``add_member()`` to ensure proper membership state.

        :param user: User to invite.
        :param admin: Admin doing the action. If provided, user is only invited
            if the object is an admin for this group. Default: None.
        :returns: Newly created Membership or None.
        """
        if admin is None or self.is_admin(admin):
            return self.add_member(user, state=MembershipState.PENDING_USER)
        return None