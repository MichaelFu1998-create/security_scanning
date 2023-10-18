def _run_generic_command(self, repo, cmd):
        """
        Run a generic command within the repo. Assumes that you are
        in the repo's root directory
        """
        
        result = None
        with cd(repo.rootdir):
            # Dont use sh. It is not collecting the stdout of all
            # child processes.
            output = self._run(cmd)
            try:
                result = {
                    'cmd': cmd,
                    'status': 'success',
                    'message': output,
                }
            except Exception as e:
                result = {
                    'cmd': cmd,
                    'status': 'error',
                    'message': str(e)
                }

        return result