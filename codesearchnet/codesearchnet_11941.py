def create_user(name, password, host='localhost', **kwargs):
    """
    Create a MySQL user.

    Example::

        import burlap

        # Create DB user if it does not exist
        if not burlap.mysql.user_exists('dbuser'):
            burlap.mysql.create_user('dbuser', password='somerandomstring')

    """
    with settings(hide('running')):
        query("CREATE USER '%(name)s'@'%(host)s' IDENTIFIED BY '%(password)s';" % {
            'name': name,
            'password': password,
            'host': host
        }, **kwargs)
    puts("Created MySQL user '%s'." % name)