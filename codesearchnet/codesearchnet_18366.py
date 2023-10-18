def auto_complete_choices(self, case_sensitive=False):
        """
        A command line auto complete similar behavior. Find all item with same
        prefix of this one.

        :param case_sensitive: toggle if it is case sensitive.
        :return: list of :class:`pathlib_mate.pathlib2.Path`.
        """
        self_basename = self.basename
        self_basename_lower = self.basename.lower()
        if case_sensitive:  # pragma: no cover
            def match(basename):
                return basename.startswith(self_basename)
        else:
            def match(basename):
                return basename.lower().startswith(self_basename_lower)

        choices = list()
        if self.is_dir():
            choices.append(self)
            for p in self.sort_by_abspath(self.select(recursive=False)):
                choices.append(p)
        else:
            p_parent = self.parent
            if p_parent.is_dir():
                for p in self.sort_by_abspath(p_parent.select(recursive=False)):
                    if match(p.basename):
                        choices.append(p)
            else:  # pragma: no cover
                raise ValueError("'%s' directory does not exist!" % p_parent)
        return choices