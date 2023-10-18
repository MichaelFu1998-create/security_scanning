def add_source(self, source_class, *constructor_args):
        """
        Adds a source to the factory provided it's type and constructor arguments
        :param source_class: The class used to instantiate the source
        :type source_class: type
        :param constructor_args: Arguments to be passed into the constructor
        :type constructor_args: Iterable
        """
        if not IIPSource.implementedBy(source_class):
            raise TypeError("source_class {} must implement IIPSource".format(source_class))
        else:
            self._sources.add((source_class, constructor_args))