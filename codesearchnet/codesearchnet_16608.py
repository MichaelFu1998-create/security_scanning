def data(self, data):
        """Overwrite the file with new data. You probably shouldn't do
        this yourself, it's easy to screw up your whole file with this."""
        if self.is_caching:
            self.cache = data
        else:
            fcontents = self.file_contents
            with open(self.path, "w") as f:
                try:
                    # Write the file. Keep user settings about indentation, etc
                    indent = self.indent if self.pretty else None
                    json.dump(data, f, sort_keys=self.sort_keys, indent=indent)
                except Exception as e:
                    # Rollback to prevent data loss
                    f.seek(0)
                    f.truncate()
                    f.write(fcontents)
                    # And re-raise the exception
                    raise e
        self._updateType()