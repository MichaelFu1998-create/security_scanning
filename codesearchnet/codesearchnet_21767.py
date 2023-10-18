def upgrade(self, package):
        '''Update a python package using pip'''

        logger.debug('Upgrading ' + package)
        shell.run(self.pip_path, 'install', '--upgrade', '--no-deps', package)
        shell.run(self.pip_path, 'install', package)