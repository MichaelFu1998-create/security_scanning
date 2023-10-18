def load_description(name, root=''):
        """
        .. warning::

            Experiment feature.

            BE CAREFUL! WE MAY REMOVE THIS FEATURE!


        Load resource file as description,
        if resource file not exist,will return empty string.

        :param str path: name resource path
        :param str root: same as `load_resource` root
        :return: `str`
        """
        desc = ''

        try:
            desc = Component.load_resource(name, root=root)
        except (IOError, ImportError):
            pass

        return desc