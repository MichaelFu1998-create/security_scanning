def get_fpath(self, cfgstr=None):
        """
        Reports the filepath that the cacher will use.
        It will attempt to use '{fname}_{cfgstr}{ext}' unless that is too long.
        Then cfgstr will be hashed.

        Example:
            >>> from ubelt.util_cache import Cacher
            >>> import pytest
            >>> with pytest.warns(UserWarning):
            >>>     cacher = Cacher('test_cacher1')
            >>>     cacher.get_fpath()
            >>> self = Cacher('test_cacher2', cfgstr='cfg1')
            >>> self.get_fpath()
            >>> self = Cacher('test_cacher3', cfgstr='cfg1' * 32)
            >>> self.get_fpath()
        """
        condensed = self._condense_cfgstr(cfgstr)
        fname_cfgstr = '{}_{}{}'.format(self.fname, condensed, self.ext)
        fpath = join(self.dpath, fname_cfgstr)
        fpath = normpath(fpath)
        return fpath