def to_special_value(self, value):
        """
        Return proper spdx term or Literal
        """
        if isinstance(value, utils.NoAssert):
            return self.spdx_namespace.noassertion
        elif isinstance(value, utils.SPDXNone):
            return self.spdx_namespace.none
        else:
            return Literal(value)