def from_string(cls, content, position=1, file_id=None):
        """
        Convenience method to create a file from a string.

        This file object's metadata will have the id 'inlined_input'.

        Inputs
        ------
        content -- the content of the file (a string).
        position -- (default 1) rank among all files of the model while parsing
            see FileMetadata
        file_id -- (default 'inlined_input') the file_id that will be used by
            kappa.
        """
        if file_id is None:
            file_id = 'inlined_input'
        return cls(FileMetadata(file_id, position), content)