def subscribe(self, user):
        """Subscribe a user to a group (done by users).

        Wrapper around ``add_member()`` which checks subscription policy.

        :param user: User to subscribe.
        :returns: Newly created Membership or None.
        """
        if self.subscription_policy == SubscriptionPolicy.OPEN:
            return self.add_member(user)
        elif self.subscription_policy == SubscriptionPolicy.APPROVAL:
            return self.add_member(user, state=MembershipState.PENDING_ADMIN)
        elif self.subscription_policy == SubscriptionPolicy.CLOSED:
            return None