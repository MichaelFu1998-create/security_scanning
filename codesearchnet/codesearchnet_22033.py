def initiate(self):
        """Sets up the :class:`AdminSite` and creates a user with the
        appropriate privileges.  This should be called from the inheritor's
        :class:`TestCase.setUp` method.
        """
        self.site = admin.sites.AdminSite()
        self.admin_user = create_admin(self.USERNAME, self.EMAIL, self.PASSWORD)
        self.authed = False