def pull(self, repo_path, *args):
        '''Clone a repository to a destination relative to envrionment root'''

        logger.debug('Pulling ' + repo_path)
        if not repo_path.startswith(self.env_path):
            repo_path = unipath(self.env_path, repo_path)

        return shell.run('git', 'pull', *args, **{'cwd': repo_path})