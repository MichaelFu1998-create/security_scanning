def resolve(self, script_name, path_info):
        """Return a _DAVResource object for the path (None, if not found).

        `path_info`: is a URL relative to this object.
        """
        if path_info in ("", "/"):
            return self
        assert path_info.startswith("/")
        name, rest = util.pop_path(path_info)
        res = self.get_member(name)
        if res is None or rest in ("", "/"):
            return res
        return res.resolve(util.join_uri(script_name, name), rest)