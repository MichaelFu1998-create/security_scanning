def register_filters(self):
        """ Register filters for Jinja to use

       .. note::  Extends the dictionary filters of jinja_env using self._filters list
        """
        for _filter, instance in self._filters:
            if not instance:
                self.app.jinja_env.filters[
                    _filter.replace("f_", "")
                ] = getattr(flask_nemo.filters, _filter)
            else:
                self.app.jinja_env.filters[
                    _filter.replace("f_", "")
                ] = getattr(instance, _filter.replace("_{}".format(instance.name), ""))