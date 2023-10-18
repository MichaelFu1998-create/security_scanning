def from_file(cls, fpath, position=1, file_id=None):
        """
        Convience method to create a kappa file object from a file on disk

        Inputs
        ------
        fpath -- path to the file on disk
        position -- (default 1) rank among all files of the model while parsing
            see FileMetadata
        file_id -- (default = fpath) the file_id that will be used by kappa.
        """
        if file_id is None:
            file_id = fpath
        with open(fpath) as f:
            code = f.read()
            file_content = str(code)
            file_metadata = FileMetadata(file_id, position)
            return cls(file_metadata, file_content)