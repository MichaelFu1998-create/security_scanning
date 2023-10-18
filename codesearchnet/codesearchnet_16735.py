def set_attr(self, name, value):
        """Implementation of attribute setting

        ``space.name = value`` by user script
        Called from ``Space.__setattr__``
        """
        if not is_valid_name(name):
            raise ValueError("Invalid name '%s'" % name)

        if name in self.namespace:
            if name in self.refs:
                if name in self.self_refs:
                    self.new_ref(name, value)
                else:
                    raise KeyError("Ref '%s' cannot be changed" % name)

            elif name in self.cells:
                if self.cells[name].is_scalar():
                    self.cells[name].set_value((), value)
                else:
                    raise AttributeError("Cells '%s' is not a scalar." % name)
            else:
                raise ValueError
        else:
            self.new_ref(name, value)