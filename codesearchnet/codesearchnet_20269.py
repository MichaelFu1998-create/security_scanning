def config(self, what='get', params=None):
        """
        Paramers:
        ---------

        workspace: Directory to store the dataset repositories
        email:
        """
        if what == 'get':
            return {
                'name': 'git',
                'nature': 'repomanager',
                'variables': [],
            }
        elif what == 'set':
            self.workspace = params['Local']['workspace']
            self.workspace = os.path.abspath(self.workspace)
            self.username = params['User']['user.name']
            self.fullname = params['User']['user.fullname']
            self.email = params['User']['user.email']

            repodir = os.path.join(self.workspace, 'datasets')
            if not os.path.exists(repodir):
                return

            for username in os.listdir(repodir):
                for reponame in os.listdir(os.path.join(repodir, username)):
                    if self.is_my_repo(username, reponame):
                        r = Repo(username, reponame)
                        r.rootdir = os.path.join(repodir, username, reponame)
                        package = os.path.join(r.rootdir, 'datapackage.json')
                        if not os.path.exists(package):
                            print("datapackage.json does not exist in dataset")
                            print("Skipping: {}/{}".format(username, reponame))
                            continue

                        packagedata = open(package).read()
                        r.package = json.JSONDecoder(object_pairs_hook=collections.OrderedDict).decode(packagedata)
                        r.manager = self
                        self.add(r)