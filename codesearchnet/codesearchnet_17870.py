def update(self, name=None, description=None, privacy_policy=None,
               subscription_policy=None, is_managed=None):
        """Update group.

        :param name: Name of group.
        :param description: Description of group.
        :param privacy_policy: PrivacyPolicy
        :param subscription_policy: SubscriptionPolicy
        :returns: Updated group
        """
        with db.session.begin_nested():
            if name is not None:
                self.name = name
            if description is not None:
                self.description = description
            if (
                privacy_policy is not None and
                PrivacyPolicy.validate(privacy_policy)
            ):
                self.privacy_policy = privacy_policy
            if (
                subscription_policy is not None and
                SubscriptionPolicy.validate(subscription_policy)
            ):
                self.subscription_policy = subscription_policy
            if is_managed is not None:
                self.is_managed = is_managed

            db.session.merge(self)

        return self