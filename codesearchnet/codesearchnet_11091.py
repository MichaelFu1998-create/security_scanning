def get_effect_class(self, class_name, package_name=None) -> Type[Effect]:
        """
        Get an effect class from the effect registry.

        Args:
            class_name (str): The exact class name of the effect

        Keyword Args:
            package_name (str): The python path to the effect package the effect name is located.
                                This is optional and can be used to avoid issue with class name collisions.

        Returns:
            Effect class
        """
        if package_name:
            return effects.find_effect_class("{}.{}".format(package_name, class_name))

        return effects.find_effect_class(class_name)