def git(self, username, repo, alias=None, token=None):
        """
        Parameters
        ----------
        token: str, default None
            Assumes you have GITHUB_TOKEN in envvar if None

        https://github.com/blog/1270-easier-builds-and-deployments-using-git-
        over-https-and-oauth
        """
        if alias is None:
            alias = repo
        if token is None:
            token = os.environ.get('GITHUB_TOKEN')
        self.wait('mkdir -p %s' % alias)
        old_dir = self.pwd
        try:
            self.chdir(alias, relative=True)
            cmd = 'git init && git pull https://%s@github.com/%s/%s.git'
            # last line to stderr
            return self.wait(cmd % (token, username, repo),
                             raise_on_error=False)
        finally:
            self.chdir(old_dir, relative=False)