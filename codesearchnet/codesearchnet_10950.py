def buffers_exist(self):
        """Checks if the bin files referenced exist"""
        for buff in self.buffers:
            if not buff.is_separate_file:
                continue

            path = self.path.parent / buff.uri
            if not os.path.exists(path):
                raise FileNotFoundError("Buffer {} referenced in {} not found".format(path, self.path))