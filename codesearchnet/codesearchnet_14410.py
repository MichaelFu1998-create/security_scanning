def _update(self, conf_dict, base_name=None):
        """ Updates the current configuration with the values in `conf_dict`.

            :param dict conf_dict: Dictionary of key value settings.
            :param str base_name: Base namespace for setting keys.

        """
        for name in conf_dict:
            # Skip private names
            if name.startswith('_'):
                continue
            value = conf_dict[name]
            # Skip Namespace if it's imported
            if value is Namespace:
                continue
            # Use a base namespace
            if base_name:
                name = base_name + '.' + name
            if isinstance(value, Namespace):
                for name, value in value.iteritems(name):
                    self.set(name, value)
            # Automatically call any functions in the settings module, and if
            # they return a value other than None, that value becomes a setting
            elif callable(value):
                value = value()
                if value is not None:
                    self.set(name, value)
            else:
                self.set(name, value)