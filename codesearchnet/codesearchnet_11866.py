def get_media_timestamp(self, last_timestamp=None):
        """
        Retrieves the most recent timestamp of the media in the static root.

        If last_timestamp is given, retrieves the first timestamp more recent than this value.
        """
        r = self.local_renderer
        _latest_timestamp = -1e9999999999999999
        for path in self.iter_static_paths():
            path = r.env.static_root + '/' + path
            self.vprint('checking timestamp of path:', path)
            if not os.path.isfile(path):
                continue
            #print('path:', path)
            _latest_timestamp = max(_latest_timestamp, get_last_modified_timestamp(path) or _latest_timestamp)
            if last_timestamp is not None and _latest_timestamp > last_timestamp:
                break
        self.vprint('latest_timestamp:', _latest_timestamp)
        return _latest_timestamp