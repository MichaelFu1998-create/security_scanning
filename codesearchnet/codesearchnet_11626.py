def runScript(self, scriptname, additional_environment=None):
        ''' Run the specified script from the scripts section of the
            module.json file in the directory of this module.
        '''
        import subprocess
        import shlex

        command = self.getScript(scriptname)
        if command is None:
            logger.debug('%s has no script %s', self, scriptname)
            return 0

        if not len(command):
            logger.error("script %s of %s is empty", scriptname, self.getName())
            return 1

        # define additional environment variables for scripts:
        env = os.environ.copy()
        if additional_environment is not None:
            env.update(additional_environment)

        errcode = 0
        child = None
        try:
            logger.debug('running script: %s', command)
            child = subprocess.Popen(
                command, cwd = self.path, env = env
            )
            child.wait()
            if child.returncode:
                logger.error(
                    "script %s (from %s) exited with non-zero status %s",
                    scriptname,
                    self.getName(),
                    child.returncode
                )
                errcode = child.returncode
            child = None
        finally:
            if child is not None:
                tryTerminate(child)
        return errcode