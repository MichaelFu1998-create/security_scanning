def _detect_or_validate(self, val):
        '''
        Detect the version used from the row content, or validate against
        the version if given.
        '''
        if isinstance(val, list) \
                or isinstance(val, dict) \
                or isinstance(val, SortableDict) \
                or isinstance(val, Grid):
            # Project Haystack 3.0 type.
            self._assert_version(VER_3_0)