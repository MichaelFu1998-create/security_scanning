def set_real_value_class(self):
        """
        value_class is initially a string with the import path to the resource class, but we need to get the actual class before doing any work

        We do not expect the actual clas to be in value_class since the beginning to avoid nasty import egg-before-chicken errors
        """
        if self.value_class is not None and isinstance(self.value_class, str):
            module_name, dot, class_name = self.value_class.rpartition(".")
            module = __import__(module_name, fromlist=[class_name])
            self.value_class = getattr(module, class_name)
            self._initialized = True