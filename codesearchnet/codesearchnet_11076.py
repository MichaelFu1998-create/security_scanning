def load_effects_classes(self):
        """Iterate the module attributes picking out effects"""
        self.effect_classes = []

        for _, cls in inspect.getmembers(self.effect_module):
            if inspect.isclass(cls):
                if cls == Effect:
                    continue

                if issubclass(cls, Effect):
                    self.effect_classes.append(cls)
                    self.effect_class_map[cls.__name__] = cls
                    cls._name = "{}.{}".format(self.effect_module_name, cls.__name__)