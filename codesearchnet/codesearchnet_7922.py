def deny(self, role, method, resource, with_children=False):
        """Add denying rules.

        :param role: Role of this rule.
        :param method: Method to deny in rule, include GET, POST, PUT etc.
        :param resource: Resource also view function.
        :param with_children: Deny role's children in rule as well
                              if with_children is `True`
        """
        if with_children:
            for r in role.get_children():
                permission = (r.get_name(), method, resource)
                if permission not in self._denied:
                    self._denied.append(permission)
        permission = (role.get_name(), method, resource)
        if permission not in self._denied:
            self._denied.append(permission)