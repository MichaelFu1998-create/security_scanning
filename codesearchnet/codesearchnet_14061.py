def ximport(self, libName):
        '''
        Import Nodebox libraries.

        The libraries get _ctx, which provides
        them with the nodebox API.

        :param libName: Library name to import
        '''
        # from Nodebox
        lib = __import__(libName)
        self._namespace[libName] = lib
        lib._ctx = self
        return lib