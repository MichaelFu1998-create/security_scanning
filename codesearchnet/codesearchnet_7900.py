def del_acl_method(self, method_name):
        """ACL system: ensure the user will not have access to that method."""
        if self.allowed_methods is None:
            raise ValueError(
                "Trying to delete an ACL method, but none were"
                + " defined yet! Or: No ACL restrictions yet, why would you"
                + " delete one?"
            )

        self.allowed_methods.remove(method_name)