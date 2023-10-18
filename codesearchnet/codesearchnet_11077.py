def load_resource_module(self):
        """Fetch the resource list"""
        # Attempt to load the dependencies module
        try:
            name = '{}.{}'.format(self.name, 'dependencies')
            self.dependencies_module = importlib.import_module(name)
        except ModuleNotFoundError as err:
            raise EffectError(
                (
                    "Effect package '{}' has no 'dependencies' module or the module has errors. "
                    "Forwarded error from importlib: {}"
                ).format(self.name, err))

        # Fetch the resource descriptions
        try:
            self.resources = getattr(self.dependencies_module, 'resources')
        except AttributeError:
            raise EffectError("Effect dependencies module '{}' has no 'resources' attribute".format(name))

        if not isinstance(self.resources, list):
            raise EffectError(
                "Effect dependencies module '{}': 'resources' is of type {} instead of a list".format(
                    name, type(self.resources)))

        # Fetch the effect class list
        try:
            self.effect_packages = getattr(self.dependencies_module, 'effect_packages')
        except AttributeError:
            raise EffectError("Effect dependencies module '{}' has 'effect_packages' attribute".format(name))

        if not isinstance(self.effect_packages, list):
            raise EffectError(
                "Effect dependencies module '{}': 'effect_packages' is of type {} instead of a list".format(
                    name, type(self.effects)))