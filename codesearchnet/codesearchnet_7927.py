def has_permission(self, method, endpoint, user=None):
        """Return does the current user can access the resource.
        Example::

            @app.route('/some_url', methods=['GET', 'POST'])
            @rbac.allow(['anonymous'], ['GET'])
            def a_view_func():
                return Response('Blah Blah...')

        If you are not logged.

        `rbac.has_permission('GET', 'a_view_func')` return True.
        `rbac.has_permission('POST', 'a_view_func')` return False.

        :param method: The method wait to check.
        :param endpoint: The application endpoint.
        :param user: user who you need to check. Current user by default.
        """
        app = self.get_app()
        _user = user or self._user_loader()
        if not hasattr(_user, 'get_roles'):
            roles = [anonymous]
        else:
            roles = _user.get_roles()
        return self._check_permission(roles, method, endpoint)