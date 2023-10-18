def create(self, name, gid=None):
        """
        Create a new group.

        Example::

            import burlap

            if not burlap.group.exists('admin'):
                burlap.group.create('admin')

        """
        args = []
        if gid:
            args.append('-g %s' % gid)
        args.append(name)
        args = ' '.join(args)
        self.sudo('groupadd --force %s || true' % args)