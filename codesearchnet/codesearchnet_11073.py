def find_effect_class(self, path) -> Type[Effect]:
        """
        Find an effect class by class name or full python path to class

        Args:
            path (str): effect class name or full python path to effect class

        Returns:
            Effect class

        Raises:
            EffectError if no class is found
        """
        package_name, class_name = parse_package_string(path)

        if package_name:
            package = self.get_package(package_name)
            return package.find_effect_class(class_name, raise_for_error=True)

        for package in self.packages:
            effect_cls = package.find_effect_class(class_name)
            if effect_cls:
                return effect_cls

        raise EffectError("No effect class '{}' found in any packages".format(class_name))