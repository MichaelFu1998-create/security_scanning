def save(self, data, cfgstr=None):
        """
        Writes data to path specified by `self.fpath(cfgstr)`.

        Metadata containing information about the cache will also be appended
        to an adjacent file with the `.meta` suffix.

        Example:
            >>> from ubelt.util_cache import *  # NOQA
            >>> # Normal functioning
            >>> cfgstr = 'long-cfg' * 32
            >>> cacher = Cacher('test_enabled_save', cfgstr)
            >>> cacher.save('data')
            >>> assert exists(cacher.get_fpath()), 'should be enabeled'
            >>> assert exists(cacher.get_fpath() + '.meta'), 'missing metadata'
            >>> # Setting the cacher as enabled=False turns it off
            >>> cacher2 = Cacher('test_disabled_save', 'params', enabled=False)
            >>> cacher2.save('data')
            >>> assert not exists(cacher2.get_fpath()), 'should be disabled'
        """
        from six.moves import cPickle as pickle
        if not self.enabled:
            return
        if self.verbose > 0:
            self.log('[cacher] ... {} cache save'.format(self.fname))

        cfgstr = self._rectify_cfgstr(cfgstr)
        condensed = self._condense_cfgstr(cfgstr)

        # Make sure the cache directory exists
        util_path.ensuredir(self.dpath)

        data_fpath = self.get_fpath(cfgstr=cfgstr)
        meta_fpath = data_fpath + '.meta'

        # Also save metadata file to reconstruct hashing
        with open(meta_fpath, 'a') as file_:
            # TODO: maybe append this in json or YML format?
            file_.write('\n\nsaving {}\n'.format(util_time.timestamp()))
            file_.write(self.fname + '\n')
            file_.write(condensed + '\n')
            file_.write(cfgstr + '\n')
            file_.write(str(self.meta) + '\n')

        with open(data_fpath, 'wb') as file_:
            # Use protocol 2 to support python2 and 3
            pickle.dump(data, file_, protocol=self.protocol)