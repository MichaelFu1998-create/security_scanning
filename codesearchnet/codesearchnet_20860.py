def load(self, source, **kwargs):
        '''Load a skeleton definition from a file.

        Parameters
        ----------
        source : str or file
            A filename or file-like object that contains text information
            describing a skeleton. See :class:`pagoda.parser.Parser` for more
            information about the format of the text file.
        '''
        if hasattr(source, 'endswith') and source.lower().endswith('.asf'):
            self.load_asf(source, **kwargs)
        else:
            self.load_skel(source, **kwargs)