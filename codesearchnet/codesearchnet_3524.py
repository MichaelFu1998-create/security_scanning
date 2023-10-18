def fromdescriptor(cls, desc):
        """
        Create a :class:`~manticore.core.workspace.Store` instance depending on the descriptor.

        Valid descriptors:
          * fs:<path>
          * redis:<hostname>:<port>
          * mem:

        :param str desc: Store descriptor
        :return: Store instance
        """
        type_, uri = ('fs', None) if desc is None else desc.split(':', 1)
        for subclass in cls.__subclasses__():
            if subclass.store_type == type_:
                return subclass(uri)
        raise NotImplementedError(f"Storage type '{type_}' not supported.")