def _set_path(self, path):
    "Set self.path, self.dirname and self.basename."
    import os.path
    self.path = os.path.abspath(path)
    self.dirname = os.path.dirname(path)
    self.basename = os.path.basename(path)