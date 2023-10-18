def auto_discover_board(self, verbose):
        """
        This method will allow up to 30 seconds for discovery (communicating with) an Arduino board
        and then will determine a pin configuration table for the board.
        :return: True if board is successfully discovered or False upon timeout
        """
        # get current time
        start_time = time.time()

        # wait for up to 30 seconds for a successful capability query to occur

        while len(self.analog_mapping_query_results) == 0:
            if time.time() - start_time > 30:
                return False
                # keep sending out a capability query until there is a response
            self.send_sysex(self.ANALOG_MAPPING_QUERY)
            time.sleep(.1)

        if verbose:
            print("Board initialized in %d seconds" % (time.time() - start_time))

        for pin in self.analog_mapping_query_results:
            self.total_pins_discovered += 1
            # non analog pins will be marked as IGNORE
            if pin != self.pymata.IGNORE:
                self.number_of_analog_pins_discovered += 1

        if verbose:
            print('Total Number of Pins Detected = %d' % self.total_pins_discovered)
            print('Total Number of Analog Pins Detected = %d' % self.number_of_analog_pins_discovered)

        # response table initialization
        # for each pin set the mode to input and the last read data value to zero
        for pin in range(0, self.total_pins_discovered):
            response_entry = [self.pymata.INPUT, 0, None]
            self.digital_response_table.append(response_entry)

        for pin in range(0, self.number_of_analog_pins_discovered):
            response_entry = [self.pymata.INPUT, 0, None]
            self.analog_response_table.append(response_entry)

        # set up latching tables
        for pin in range(0, self.total_pins_discovered):
            digital_latch_table_entry = [0, 0, 0, 0, None]
            self.digital_latch_table.append(digital_latch_table_entry)

        for pin in range(0, self.number_of_analog_pins_discovered):
            analog_latch_table_entry = [0, 0, 0, 0, 0, None]
            self.analog_latch_table.append(analog_latch_table_entry)

        return True