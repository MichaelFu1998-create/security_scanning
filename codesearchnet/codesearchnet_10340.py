def _canonicalize(self, filename):
        """Use .collection as extension unless provided"""
        path, ext = os.path.splitext(filename)
        if not ext:
            ext = ".collection"
        return path + ext