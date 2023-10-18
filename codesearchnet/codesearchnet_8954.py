def _add_unique_file(self, item):
        """
        adds a file in self.config['files'] only if not present already
        """
        if item not in self.config['files']:
            self.config['files'].append(item)