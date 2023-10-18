def digital_message(self, data):
        """
        This method handles the incoming digital message.
        It stores the data values in the digital response table.
        Data is stored for all 8 bits of a  digital port

        :param data: Message data from Firmata

        :return: No return value.
        """
        port = data[0]
        port_data = (data[self.MSB] << 7) + data[self.LSB]

        # set all the pins for this reporting port
        # get the first pin number for this report
        pin = port * 8
        for pin in range(pin, min(pin + 8, self.total_pins_discovered)):
            # shift through all the bit positions and set the digital response table
            with self.pymata.data_lock:
                # look at the previously stored value for this pin
                prev_data = self.digital_response_table[pin][self.RESPONSE_TABLE_PIN_DATA_VALUE]
                # get the current value
                self.digital_response_table[pin][self.RESPONSE_TABLE_PIN_DATA_VALUE] = port_data & 0x01
                # if the values differ and callback is enabled for the pin, then send out the callback
                if prev_data != port_data & 0x01:
                    callback = self.digital_response_table[pin][self.RESPONSE_TABLE_CALLBACK]
                    if callback:
                        callback([self.pymata.DIGITAL, pin,
                                  self.digital_response_table[pin][self.RESPONSE_TABLE_PIN_DATA_VALUE]])

                # determine if the latch data table needs to be updated for each pin
                latching_entry = self.digital_latch_table[pin]
                if latching_entry[self.LATCH_STATE] == self.LATCH_ARMED:
                    if latching_entry[self.LATCHED_THRESHOLD_TYPE] == self.DIGITAL_LATCH_LOW:
                        if (port_data & 0x01) == 0:
                            if latching_entry[self.DIGITAL_LATCH_CALLBACK] is not None:
                                self.digital_latch_table[pin] = [0, 0, 0, 0, None]
                                latching_entry[self.DIGITAL_LATCH_CALLBACK](
                                    [self.pymata.OUTPUT | self.pymata.LATCH_MODE,
                                     pin, 0, time.time()])

                            else:
                                updated_latch_entry = latching_entry
                                updated_latch_entry[self.LATCH_STATE] = self.LATCH_LATCHED
                                updated_latch_entry[self.DIGITAL_LATCHED_DATA] = self.DIGITAL_LATCH_LOW
                                # time stamp it
                                updated_latch_entry[self.DIGITAL_TIME_STAMP] = time.time()
                        else:
                            pass
                    elif latching_entry[self.LATCHED_THRESHOLD_TYPE] == self.DIGITAL_LATCH_HIGH:
                        if port_data & 0x01:
                            if latching_entry[self.DIGITAL_LATCH_CALLBACK] is not None:
                                self.digital_latch_table[pin] = [0, 0, 0, 0, None]
                                latching_entry[self.DIGITAL_LATCH_CALLBACK](
                                    [self.pymata.OUTPUT | self.pymata.LATCH_MODE,
                                     pin, 1, time.time()])
                            else:
                                updated_latch_entry = latching_entry
                                updated_latch_entry[self.LATCH_STATE] = self.LATCH_LATCHED
                                updated_latch_entry[self.DIGITAL_LATCHED_DATA] = self.DIGITAL_LATCH_HIGH
                                # time stamp it
                                updated_latch_entry[self.DIGITAL_TIME_STAMP] = time.time()
                        else:
                            pass
                else:
                    pass

            # get the next data bit
            port_data >>= 1