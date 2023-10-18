def _rc_renamenx(self, src, dst):
        "Rename key ``src`` to ``dst`` if ``dst`` doesn't already exist"
        if self.exists(dst):
            return False

        return self._rc_rename(src, dst)