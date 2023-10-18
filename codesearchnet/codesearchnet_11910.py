def get_logs_between_commits(self, a, b):
        """
        Retrieves all commit messages for all commits between the given commit numbers
        on the current branch.
        """
        print('REAL')
        ret = self.local('git --no-pager log --pretty=oneline %s...%s' % (a, b), capture=True)
        if self.verbose:
            print(ret)
        return str(ret)