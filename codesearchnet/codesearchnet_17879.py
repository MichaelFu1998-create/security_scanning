def is_member(self, user, with_pending=False):
        """Verify if given user is a group member.

        :param user: User to be checked.
        :param bool with_pending: Whether to include pending users or not.
        :returns: True or False.
        """
        m = Membership.get(self, user)
        if m is not None:
            if with_pending:
                return True
            elif m.state == MembershipState.ACTIVE:
                return True
        return False