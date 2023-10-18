def _load_expansion(self, key, root, pattern):
        """
        Loads the files that match the given pattern.
        """
        path_pattern = os.path.join(root, pattern)
        expanded_paths = self._expand_pattern(path_pattern)

        specs=[]
        for (path, tags) in expanded_paths:
            filelist = [os.path.join(path,f) for f in os.listdir(path)] if os.path.isdir(path) else [path]
            for filepath in filelist:
                specs.append(dict(tags,**{key:os.path.abspath(filepath)}))

        return sorted(specs, key=lambda s: s[key])