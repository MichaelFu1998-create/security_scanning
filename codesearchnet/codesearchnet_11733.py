def togroups(self, user, groups):
        """
        Adds the user to the given list of groups.
        """

        r = self.local_renderer

        if isinstance(groups, six.string_types):
            groups = [_.strip() for _ in groups.split(',') if _.strip()]
        for group in groups:
            r.env.username = user
            r.env.group = group
            r.sudo('groupadd --force {group}')
            r.sudo('adduser {username} {group}')