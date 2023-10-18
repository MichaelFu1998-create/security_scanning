def get_filename(self, *parts):
        '''
        Returns an absolute filename in the data-directory (standardized by StandardizePath).

        @params parts: list(unicode)
            Path parts. Each part is joined to form a path.

        :rtype: unicode
        :returns:
            The full path prefixed with the data-directory.

        @remarks:
            This method triggers the data-directory creation.
        '''
        from zerotk.easyfs import StandardizePath

        result = [self._data_dir] + list(parts)
        result = '/'.join(result)
        return StandardizePath(result)