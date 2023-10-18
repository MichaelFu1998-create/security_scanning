def install(self, package):
        '''Install a python package using pip'''

        logger.debug('Installing ' + package)
        shell.run(self.pip_path, 'install',  package)