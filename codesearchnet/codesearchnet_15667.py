def python_value(self, value):
        """
        Convert binary blob to UUID instance
        """
        value = super(OrderedUUIDField, self).python_value(value)
        u = binascii.b2a_hex(value)
        value = u[8:16] + u[4:8] + u[0:4] + u[16:22] + u[22:32]
        return UUID(value.decode())