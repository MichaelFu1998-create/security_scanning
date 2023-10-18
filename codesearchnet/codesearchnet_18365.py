def is_empty(self, strict=True):
        """
        - If it's a file, check if it is a empty file. (0 bytes content)
        - If it's a directory, check if there's no file and dir in it.
            But if ``strict = False``, then only check if there's no file in it.

        :param strict: only useful when it is a directory. if True, only
            return True if this dir has no dir and file. if False, return True
            if it doesn't have any file.
        """
        if self.exists():
            if self.is_file():
                return self.size == 0
            elif self.is_dir():
                if strict:
                    return len(list(self.select(recursive=True))) == 0
                else:  # pragma: no cover
                    return len(list(self.select_file(recursive=True))) == 0
            else:  # pragma: no cover
                msg = "'%s' is not either file or directory! (maybe simlink)" % self
                raise EnvironmentError(msg)
        else:
            raise EnvironmentError("'%s' not exists!" % self)