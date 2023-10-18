def existing_versions(self):
        """
        Returns data with different cfgstr values that were previously computed
        with this cacher.

        Example:
            >>> from ubelt.util_cache import Cacher
            >>> # Ensure that some data exists
            >>> known_fnames = set()
            >>> cacher = Cacher('versioned_data', cfgstr='1')
            >>> cacher.ensure(lambda: 'data1')
            >>> known_fnames.add(cacher.get_fpath())
            >>> cacher = Cacher('versioned_data', cfgstr='2')
            >>> cacher.ensure(lambda: 'data2')
            >>> known_fnames.add(cacher.get_fpath())
            >>> # List previously computed configs for this type
            >>> from os.path import basename
            >>> cacher = Cacher('versioned_data', cfgstr='2')
            >>> exist_fpaths = set(cacher.existing_versions())
            >>> exist_fnames = list(map(basename, exist_fpaths))
            >>> print(exist_fnames)
            >>> assert exist_fpaths == known_fnames

            ['versioned_data_1.pkl', 'versioned_data_2.pkl']
        """
        import glob
        pattern = join(self.dpath, self.fname + '_*' + self.ext)
        for fname in glob.iglob(pattern):
            data_fpath = join(self.dpath, fname)
            yield data_fpath