def bootstrap(self, force=0):
        """
        Installs all the necessary packages necessary for managing virtual
        environments with pip.
        """
        force = int(force)
        if self.has_pip() and not force:
            return

        r = self.local_renderer

        if r.env.bootstrap_method == GET_PIP:
            r.sudo('curl --silent --show-error --retry 5 https://bootstrap.pypa.io/get-pip.py | python')
        elif r.env.bootstrap_method == EZ_SETUP:
            r.run('wget http://peak.telecommunity.com/dist/ez_setup.py -O /tmp/ez_setup.py')
            with self.settings(warn_only=True):
                r.sudo('python /tmp/ez_setup.py -U setuptools')
            r.sudo('easy_install -U pip')
        elif r.env.bootstrap_method == PYTHON_PIP:
            r.sudo('apt-get install -y python-pip')
        else:
            raise NotImplementedError('Unknown pip bootstrap method: %s' % r.env.bootstrap_method)

        r.sudo('pip {quiet_flag} install --upgrade pip')
        r.sudo('pip {quiet_flag} install --upgrade virtualenv')