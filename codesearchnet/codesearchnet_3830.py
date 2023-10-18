def clear(self, cfgstr=None):
        """
        Removes the saved cache and metadata from disk
        """
        data_fpath = self.get_fpath(cfgstr)
        if self.verbose > 0:
            self.log('[cacher] clear cache')
        if exists(data_fpath):
            if self.verbose > 0:
                self.log('[cacher] removing {}'.format(data_fpath))
            os.remove(data_fpath)

            # Remove the metadata if it exists
            meta_fpath = data_fpath + '.meta'
            if exists(meta_fpath):
                os.remove(meta_fpath)
        else:
            if self.verbose > 0:
                self.log('[cacher] ... nothing to clear')