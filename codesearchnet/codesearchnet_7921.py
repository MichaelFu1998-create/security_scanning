def allow(self, role, method, resource, with_children=True):
        """Add allowing rules.

        :param role: Role of this rule.
        :param method: Method to allow in rule, include GET, POST, PUT etc.
        :param resource: Resource also view function.
        :param with_children: Allow role's children in rule as well
                              if with_children is `True`
        """
        if with_children:
            for r in role.get_children():
                permission = (r.get_name(), method, resource)
                if permission not in self._allowed:
                    self._allowed.append(permission)
        if role == 'anonymous':
            permission = (role, method, resource)
        else:
            permission = (role.get_name(), method, resource)
        if permission not in self._allowed:
            self._allowed.append(permission)