def get_enterprise_user_id(self, obj):
        """
        Get enterprise user id from user object.

        Arguments:
            obj (User): Django User object

        Returns:
            (int): Primary Key identifier for enterprise user object.
        """
        # An enterprise learner can not belong to multiple enterprise customer at the same time
        # but if such scenario occurs we will pick the first.
        enterprise_learner = EnterpriseCustomerUser.objects.filter(user_id=obj.id).first()

        return enterprise_learner and enterprise_learner.id