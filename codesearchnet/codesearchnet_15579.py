def fetch_github_token(self):
        """
        Fetch GitHub token. First try to use variable provided
        by --token option, otherwise try to fetch it from git config
        and last CHANGELOG_GITHUB_TOKEN env variable.

        :returns: Nothing
        """

        if not self.options.token:
            try:
                for v in GH_CFG_VARS:
                    cmd = ['git', 'config', '--get', '{0}'.format(v)]
                    self.options.token = subprocess.Popen(
                        cmd, stdout=subprocess.PIPE).communicate()[0].strip()
                    if self.options.token:
                        break
            except (subprocess.CalledProcessError, WindowsError):
                pass
        if not self.options.token:
            self.options.token = os.environ.get(CHANGELOG_GITHUB_TOKEN)
        if not self.options.token:
            print(NO_TOKEN_PROVIDED)