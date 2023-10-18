def add_files(self, repo, files):
        """
        Add files to the repo
        """
        rootdir = repo.rootdir
        for f in files:
            relativepath = f['relativepath']
            sourcepath = f['localfullpath']
            if sourcepath is None:
                # This can happen if the relative path is a URL
                continue #
            # Prepare the target path
            targetpath = os.path.join(rootdir, relativepath)
            try:
                os.makedirs(os.path.dirname(targetpath))
            except:
                pass
            # print(sourcepath," => ", targetpath)
            print("Updating: {}".format(relativepath))
            shutil.copyfile(sourcepath, targetpath)
            with cd(repo.rootdir):
                self._run(['add', relativepath])