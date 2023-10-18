def clear_dir(self, path):
        """
        Deletes the given relative path using the destination storage backend.
        """
        dirs, files = self.storage.listdir(path)
        for f in files:
            fpath = os.path.join(path, f)
            if self.dry_run:
                self.log("Pretending to delete '%s'" %
                         smart_text(fpath), level=1)
            else:
                self.log("Deleting '%s'" % smart_text(fpath), level=1)
                self.storage.delete(fpath)
        for d in dirs:
            self.clear_dir(os.path.join(path, d))