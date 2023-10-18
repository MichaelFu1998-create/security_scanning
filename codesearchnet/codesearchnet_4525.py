def execute_wait(self, cmd, walltime=None, envs={}):
        ''' Synchronously execute a commandline string on the shell.

        Args:
            - cmd (string) : Commandline string to execute
            - walltime (int) : walltime in seconds, this is not really used now.

        Kwargs:
            - envs (dict) : Dictionary of env variables. This will be used
              to override the envs set at channel initialization.

        Returns:
            - retcode : Return code from the execution, -1 on fail
            - stdout  : stdout string
            - stderr  : stderr string

        Raises:
        None.
        '''
        retcode = -1
        stdout = None
        stderr = None

        current_env = copy.deepcopy(self._envs)
        current_env.update(envs)

        try:
            proc = subprocess.Popen(
                cmd,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                cwd=self.userhome,
                env=current_env,
                shell=True
            )
            proc.wait(timeout=walltime)
            stdout = proc.stdout.read()
            stderr = proc.stderr.read()
            retcode = proc.returncode

        except Exception as e:
            print("Caught exception: {0}".format(e))
            logger.warn("Execution of command [%s] failed due to \n %s ", cmd, e)
            # Set retcode to non-zero so that this can be handled in the provider.
            if retcode == 0:
                retcode = -1
            return (retcode, None, None)

        return (retcode, stdout.decode("utf-8"), stderr.decode("utf-8"))