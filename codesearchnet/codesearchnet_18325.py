def is_not_exist_or_allow_overwrite(self, overwrite=False):
        """
        Test whether a file target is not exists or it exists but allow
        overwrite.
        """
        if self.exists() and overwrite is False:
            return False
        else:  # pragma: no cover
            return True