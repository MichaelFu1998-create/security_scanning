def delete(self, repo, args=[]):
        """
        Delete files from the repo
        """

        result = None
        with cd(repo.rootdir):
            try:
                cmd = ['rm'] + list(args)
                result = {
                    'status': 'success',
                    'message': self._run(cmd)
                }
            except Exception as e:
                result = {
                    'status': 'error',
                    'message': str(e)
                }

            # print(result)
            return result