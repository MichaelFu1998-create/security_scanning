def add_package(self, name):
        """
        Registers a single package

        :param name: (str) The effect package to add
        """
        name, cls_name = parse_package_string(name)

        if name in self.package_map:
            return

        package = EffectPackage(name)
        package.load()

        self.packages.append(package)
        self.package_map[package.name] = package

        # Load effect package dependencies
        self.polulate(package.effect_packages)