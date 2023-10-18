def _cleanup(self, to_clean, allow=()):
        """ Remove keys we added for internal use
        """
        # this item's been retrieved from the API, we only need the 'data'
        # entry
        if to_clean.keys() == ["links", "library", "version", "meta", "key", "data"]:
            to_clean = to_clean["data"]
        return dict(
            [
                [k, v]
                for k, v in list(to_clean.items())
                if (k in allow or k not in self.temp_keys)
            ]
        )