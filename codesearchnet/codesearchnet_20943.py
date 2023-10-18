def get_func(self, path):
        """
        :return: (func, methods)
        """
        for url_match, func_pair in self._urls_regex_map.items():
            m = url_match.match(path)
            if m is not None:
                return func_pair.func, func_pair.methods, m.groupdict()
        return None, None, None