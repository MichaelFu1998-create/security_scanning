def get_package(self, name) -> 'EffectPackage':
        """
        Get a package by python path. Can also contain path to an effect.

        Args:
            name (str): Path to effect package or effect

        Returns:
            The requested EffectPackage

        Raises:
            EffectError when no package is found
        """
        name, cls_name = parse_package_string(name)

        try:
            return self.package_map[name]
        except KeyError:
            raise EffectError("No package '{}' registered".format(name))