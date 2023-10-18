def __register_library(self, module_name: str, attr: str, fallback: str = None):
        """Inserts Interpreter Library of imports into sketch in a very non-consensual way"""

        # Import the module Named in the string
        try:
            module = importlib.import_module(module_name)

        # If module is not found it checks if an alternative is is listed
        # If it is then it substitutes it, just so that the code can run
        except ImportError:
            if fallback is not None:
                module = importlib.import_module(fallback)
                self.__logger.warn(module_name + " not available: Replaced with " + fallback)
            else:
                self.__logger.warn(module_name + " not available: No Replacement Specified")

        # Cram the module into the __sketch in the form of module -> "attr"
        # AKA the same as `import module as attr`
        if not attr in dir(self.__sketch):
            setattr(self.__sketch, attr, module)
        else:
            self.__logger.warn(attr +" could not be imported as it's label is already used in the sketch")