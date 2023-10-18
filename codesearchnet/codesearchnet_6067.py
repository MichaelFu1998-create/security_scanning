def get_resource_inst(self, path, environ):
        """Return _VirtualResource object for path.

        path is expected to be
            categoryType/category/name/artifact
        for example:
            'by_tag/cool/My doc 2/info.html'

        See DAVProvider.get_resource_inst()
        """
        _logger.info("get_resource_inst('%s')" % path)
        self._count_get_resource_inst += 1
        root = RootCollection(environ)
        return root.resolve("", path)