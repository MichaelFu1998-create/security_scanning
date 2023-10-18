def get_effect_class(self, effect_name: str, package_name: str = None) -> Type['Effect']:
        """
        Get an effect class by the class name

        Args:
            effect_name (str): Name of the effect class

        Keyword Args:
            package_name (str): The package the effect belongs to. This is optional and only
                                needed when effect class names are not unique.

        Returns:
            :py:class:`Effect` class
        """
        return self._project.get_effect_class(effect_name, package_name=package_name)