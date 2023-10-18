def pin_state_query(self, pin):
        """
        This method issues a pin state query command. Data returned is retrieved via
        a call to get_pin_state_query_results()
        :param pin: pin number
        """
        self._command_handler.send_sysex(self._command_handler.PIN_STATE_QUERY, [pin])