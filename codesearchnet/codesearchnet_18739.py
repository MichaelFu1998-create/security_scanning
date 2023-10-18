def contribute_to_class(self, cls, name):
        """
        I need a way to ensure that this signal gets created for all child
        models, and since model inheritance doesn't have a 'contrubite_to_class'
        style hook, I am creating a fake virtual field which will be added to
        all subclasses and handles creating the signal
        """
        super(EmbeddedMediaField, self).contribute_to_class(cls, name)
        register_field(cls, self)
        
        # add a virtual field that will create signals on any/all subclasses
        cls._meta.add_virtual_field(EmbeddedSignalCreator(self))