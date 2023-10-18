def read_register(self, register):
        """
        Dynamic interface for reading cpu registers

        :param str register: register name (as listed in `self.all_registers`)
        :return: register value
        :rtype: int or long or Expression
        """
        self._publish('will_read_register', register)
        value = self._regfile.read(register)
        self._publish('did_read_register', register, value)
        return value