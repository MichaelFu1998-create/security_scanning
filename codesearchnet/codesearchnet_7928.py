def allow(self, roles, methods, with_children=True):
        """This is a decorator function.

        You can allow roles to access the view func with it.

        An example::

            @app.route('/website/setting', methods=['GET', 'POST'])
            @rbac.allow(['administrator', 'super_user'], ['GET', 'POST'])
            def website_setting():
                return Response('Setting page.')

        :param roles: List, each name of roles. Please note that,
                      `anonymous` is refered to anonymous.
                      If you add `anonymous` to the rule,
                      everyone can access the resource,
                      unless you deny other roles.
        :param methods: List, each name of methods.
                        methods is valid in ['GET', 'POST', 'PUT', 'DELETE']
        :param with_children: Whether allow children of roles as well.
                              True by default.
        """
        def decorator(view_func):
            _methods = [m.upper() for m in methods]
            for r, m, v in itertools.product(roles, _methods, [view_func.__name__]):
                self.before_acl['allow'].append((r, m, v, with_children))
            return view_func
        return decorator