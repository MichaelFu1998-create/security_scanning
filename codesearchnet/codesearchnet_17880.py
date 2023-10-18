def can_see_members(self, user):
        """Determine if given user can see other group members.

        :param user: User to be checked.
        :returns: True or False.
        """
        if self.privacy_policy == PrivacyPolicy.PUBLIC:
            return True
        elif self.privacy_policy == PrivacyPolicy.MEMBERS:
            return self.is_member(user) or self.is_admin(user)
        elif self.privacy_policy == PrivacyPolicy.ADMINS:
            return self.is_admin(user)