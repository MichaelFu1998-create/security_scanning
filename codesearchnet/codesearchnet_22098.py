def get_or_create_index(self, index_ratio, index_width):
        """Return an open file-object to the index file"""
        if not self.index_path.exists() or not self.filepath.stat().st_mtime == self.index_path.stat().st_mtime:
            create_index(self.filepath, self.index_path, index_ratio=index_ratio, index_width=index_width)
        return IndexFile(str(self.index_path))