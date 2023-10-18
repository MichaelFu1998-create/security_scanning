def write_register(self, register, value):
        """
        Dynamic interface for writing cpu registers

        :param str register: register name (as listed in `self.all_registers`)
        :param value: register value
        :type value: int or long or Expression
        """
        self._publish('will_write_register', register, value)
        value = self._regfile.write(register, value)
        self._publish('did_write_register', register, value)
        return value