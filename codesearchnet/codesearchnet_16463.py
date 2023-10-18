def _ignore_path(cls, path, ignore_list=None, white_list=None):
        """Returns a whether a path should be ignored or not."""
        ignore_list = ignore_list or []
        white_list = white_list or []
        return (cls._matches_patterns(path, ignore_list) and
                not cls._matches_patterns(path, white_list))