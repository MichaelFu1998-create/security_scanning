def from_pattern(cls, pattern, filetype=None, key='filename', root=None, ignore=[]):
        """
        Convenience method to directly chain a pattern processed by
        FilePattern into a FileInfo instance.

        Note that if a default filetype has been set on FileInfo, the
        filetype argument may be omitted.
        """
        filepattern = FilePattern(key, pattern, root=root)
        if FileInfo.filetype and filetype is None:
            filetype = FileInfo.filetype
        elif filetype is None:
            raise Exception("The filetype argument must be supplied unless "
                            "an appropriate default has been specified as "
                            "FileInfo.filetype")
        return FileInfo(filepattern, key, filetype, ignore=ignore)