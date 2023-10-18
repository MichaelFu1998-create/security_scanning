def get_property_value(self, name):
        """Return the value of a property.

        See get_property_value()
        """
        # Supported custom live properties
        if name == "{hg:}branch":
            return self.fctx.branch()
        elif name == "{hg:}date":
            # (secs, tz-ofs)
            return compat.to_native(self.fctx.date()[0])
        elif name == "{hg:}description":
            return self.fctx.description()
        elif name == "{hg:}filerev":
            return compat.to_native(self.fctx.filerev())
        elif name == "{hg:}rev":
            return compat.to_native(self.fctx.rev())
        elif name == "{hg:}user":
            return compat.to_native(self.fctx.user())

        # Let base class implementation report live and dead properties
        return super(HgResource, self).get_property_value(name)