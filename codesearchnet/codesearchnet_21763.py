def find_repos(self, depth=10):
        '''Get all git repositories within this environment'''

        repos = []

        for root, subdirs, files in walk_dn(self.root, depth=depth):
            if 'modules' in root:
                continue
            if '.git' in subdirs:
                repos.append(root)

        return repos