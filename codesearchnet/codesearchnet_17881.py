def can_invite_others(self, user):
        """Determine if user can invite people to a group.

        Be aware that this check is independent from the people (users) which
        are going to be invited. The checked user is the one who invites
        someone, NOT who is going to be invited.

        :param user: User to be checked.
        :returns: True or False.
        """
        if self.is_managed:
            return False
        elif self.is_admin(user):
            return True
        elif self.subscription_policy != SubscriptionPolicy.CLOSED:
            return True
        else:
            return False