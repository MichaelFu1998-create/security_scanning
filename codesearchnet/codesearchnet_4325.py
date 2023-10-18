def to_special_value(self, value):
        """Checks if value is a special SPDX value such as
        NONE, NOASSERTION or UNKNOWN if so returns proper model.
        else returns value"""
        if value == self.spdx_namespace.none:
            return utils.SPDXNone()
        elif value == self.spdx_namespace.noassertion:
            return utils.NoAssert()
        elif value == self.spdx_namespace.unknown:
            return utils.UnKnown()
        else:
            return value