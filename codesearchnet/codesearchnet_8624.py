def get_enterprise_sso_uid(self, obj):
        """
        Get enterprise SSO UID.

        Arguments:
            obj (User): Django User object

        Returns:
            (str): string containing UUID for enterprise customer's Identity Provider.
        """
        # An enterprise learner can not belong to multiple enterprise customer at the same time
        # but if such scenario occurs we will pick the first.
        enterprise_learner = EnterpriseCustomerUser.objects.filter(user_id=obj.id).first()

        return enterprise_learner and enterprise_learner.get_remote_id()