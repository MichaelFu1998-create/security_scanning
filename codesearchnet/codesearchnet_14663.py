def export(self, output_path=None, decrypt=False):
        """Export all keys in the stash to a list or a file
        """
        self._assert_valid_stash()

        all_keys = []
        for key in self.list():
            # We `dict` this as a precaution as tinydb returns
            # a tinydb.database.Element instead of a dictionary
            # and well.. I ain't taking no chances
            all_keys.append(dict(self.get(key, decrypt=decrypt)))
        if all_keys:
            if output_path:
                with open(output_path, 'w') as output_file:
                    output_file.write(json.dumps(all_keys, indent=4))
            return all_keys
        else:
            raise GhostError('There are no keys to export')