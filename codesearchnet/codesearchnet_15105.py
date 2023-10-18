def _relative_to_absolute(self, module_location, folder):
        """:return: the absolute path for the `folder` relative to
        the module_location.
        :rtype: str
        """
        if os.path.isfile(module_location):
            path = os.path.dirname(module_location)
        elif os.path.isdir(module_location):
            path = module_location
        else:
            module_folder = os.path.dirname(module_location)
            if module_folder:
                path = module_folder
            else:
                __import__(module_location)
                module = sys.modules[module_location]
                path = os.path.dirname(module.__file__)
        absolute_path = os.path.join(path, folder)
        return absolute_path