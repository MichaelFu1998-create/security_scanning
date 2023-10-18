def get_pin_state_query_results(self):
        """
        This method returns the results of a previous call to pin_state_query() and then resets
        the pin state query data to None

        :return: Raw pin state query data
        """
        r_data = self._command_handler.last_pin_query_results
        self._command_handler.last_pin_query_results = []
        return r_data