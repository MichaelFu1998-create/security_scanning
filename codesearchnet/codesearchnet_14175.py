def import_libs(self, module_names, impl_name):
        """
        Loop through module_names,
        add has_.... booleans to class
        set ..._impl to first successful import

        :param module_names:  list of module names to try importing
        :param impl_name:  used in error output if no modules succeed
        :return: name, module from first successful implementation
        """
        for name in module_names:
            try:
                module = __import__(name)
                has_module = True
            except ImportError:
                module = None
                has_module = False
            setattr(self, name, module)
            setattr(self, 'has_%s' % name, has_module)

        for name in module_names:
            try:
                return name, __import__(name)
            except ImportError:
                pass
        raise ImportError('No %s Implementation found, tried: %s' % (impl_name, ' '.join(module_names)))