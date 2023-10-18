def clone(self, repo_path, destination, branch=None):
        '''Clone a repository to a destination relative to envrionment root'''

        logger.debug('Installing ' + repo_path)
        if not destination.startswith(self.env_path):
            destination = unipath(self.env_path, destination)

        if branch:
            return shell.run('git', 'clone', repo_path, '--branch', branch,
                             '--single-branch', '--recursive', destination)

        return shell.run('git', 'clone', '--recursive', repo_path, destination)