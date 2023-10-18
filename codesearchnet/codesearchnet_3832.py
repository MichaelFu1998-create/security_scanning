def load(self, cfgstr=None):
        """
        Loads the data

        Raises:
            IOError - if the data is unable to be loaded. This could be due to
                a cache miss or because the cache is disabled.

        Example:
            >>> from ubelt.util_cache import *  # NOQA
            >>> # Setting the cacher as enabled=False turns it off
            >>> cacher = Cacher('test_disabled_load', '', enabled=True)
            >>> cacher.save('data')
            >>> assert cacher.load() == 'data'
            >>> cacher.enabled = False
            >>> assert cacher.tryload() is None
        """
        from six.moves import cPickle as pickle
        cfgstr = self._rectify_cfgstr(cfgstr)

        dpath = self.dpath
        fname = self.fname
        verbose = self.verbose

        if not self.enabled:
            if verbose > 1:
                self.log('[cacher] ... cache disabled: fname={}'.format(self.fname))
            raise IOError(3, 'Cache Loading Is Disabled')

        fpath = self.get_fpath(cfgstr=cfgstr)

        if not exists(fpath):
            if verbose > 2:
                self.log('[cacher] ... cache does not exist: '
                         'dpath={} fname={} cfgstr={}'.format(
                             basename(dpath), fname, cfgstr))
            raise IOError(2, 'No such file or directory: %r' % (fpath,))
        else:
            if verbose > 3:
                self.log('[cacher] ... cache exists: '
                         'dpath={} fname={} cfgstr={}'.format(
                             basename(dpath), fname, cfgstr))
        try:
            with open(fpath, 'rb') as file_:
                data = pickle.load(file_)
        except Exception as ex:
            if verbose > 0:
                self.log('CORRUPTED? fpath = %s' % (fpath,))
            if verbose > 1:
                self.log('[cacher] ... CORRUPTED? dpath={} cfgstr={}'.format(
                    basename(dpath), cfgstr))
            if isinstance(ex, (EOFError, IOError, ImportError)):
                raise IOError(str(ex))
            else:
                if verbose > 1:
                    self.log('[cacher] ... unknown reason for exception')
                raise
        else:
            if self.verbose > 2:
                self.log('[cacher] ... {} cache hit'.format(self.fname))
            elif verbose > 1:
                self.log('[cacher] ... cache hit')
        return data