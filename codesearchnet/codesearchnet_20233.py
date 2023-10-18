def search(self, what, name=None, version=None):
        """
        Search for a plugin
        """
        filtered = {}

        # The search may for a scan (what is None) or
        if what is None:
            whats = list(self.plugins.keys())
        elif what is not None:
            if what not in self.plugins:
                raise Exception("Unknown class of plugins")
            whats = [what]
        for what in whats:
            if what not in filtered:
                filtered[what] = []
            for key in self.plugins[what].keys():
                (k_name, k_version) = key
                if name is not None and k_name != name:
                    continue
                if version is not None and k_version != version:
                    continue
                if self.plugins[what][key].enable == 'n':
                    continue
                filtered[what].append(key)

        # print(filtered)
        return filtered