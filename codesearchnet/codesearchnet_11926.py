def check_ok(self):
        """
        Ensures all tests have passed for this branch.

        This should be called before deployment, to prevent accidental deployment of code
        that hasn't passed automated testing.
        """
        import requests

        if not self.env.check_ok:
            return

        # Find current git branch.
        branch_name = self._local('git rev-parse --abbrev-ref HEAD', capture=True).strip()

        check_ok_paths = self.env.check_ok_paths or {}

        if branch_name in check_ok_paths:
            check = check_ok_paths[branch_name]
            if 'username' in check:
                auth = (check['username'], check['password'])
            else:
                auth = None
            ret = requests.get(check['url'], auth=auth)
            passed = check['text'] in ret.content
            assert passed, 'Check failed: %s' % check['url']