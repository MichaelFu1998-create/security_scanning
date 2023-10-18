def backup(self, path):
        """Backup all files from the device"""
        log.info('Backing up in '+path)
        # List file to backup
        files = self.file_list()
        # then download each of then
        self.prepare()
        for f in files:
            self.read_file(f[0], os.path.join(path, f[0]))