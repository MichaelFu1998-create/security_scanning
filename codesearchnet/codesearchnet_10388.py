def _init_filename(self, filename=None, ext=None):
        """Initialize the current filename :attr:`FileUtils.real_filename` of the object.

        Bit of a hack.

        - The first invocation must have ``filename != None``; this will set a
          default filename with suffix :attr:`FileUtils.default_extension`
          unless another one was supplied.

        - Subsequent invocations either change the filename accordingly or
          ensure that the default filename is set with the proper suffix.

        """

        extension = ext or self.default_extension
        filename = self.filename(filename, ext=extension, use_my_ext=True, set_default=True)
        #: Current full path of the object for reading and writing I/O.
        self.real_filename = os.path.realpath(filename)