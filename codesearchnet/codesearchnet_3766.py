def revoke(self, fail_on_found=False, **kwargs):
        """Remove a user or a team from a role. Required information:
        1) Type of the role
        2) Resource of the role, inventory, credential, or any other
        3) A user or a team to add to the role

        =====API DOCS=====
        Remove a user or a team from a role. Required information:
        * Type of the role.
        * Resource of the role, inventory, credential, or any other.
        * A user or a team to add to the role.

        :param fail_on_found: Flag that if set, the operation fails if a user/team dose not have the role.
        :type fail_on_found: bool
        :param `**kwargs`: The user to be disassociated and the role to disassociate.
        :returns: parsed JSON of role revoke.
        :rtype: dict

        =====API DOCS=====
        """
        return self.role_write(fail_on_found=fail_on_found,
                               disassociate=True, **kwargs)