def analog_message(self, data):
        """
        This method handles the incoming analog data message.
        It stores the data value for the pin in the analog response table.
        If a callback function was associated with this pin, the callback function is invoked.
        This method also checks to see if latching was requested for the pin. If the latch criteria was met,
        the latching table is updated. If a latching callback function was provided by the user, a latching
        notification callback message is sent to the user in place of updating the latching table.

        :param data: Message data from Firmata

        :return: No return value.
        """
        with self.pymata.data_lock:
            # hold on to the previous value
            previous_value = \
                self.analog_response_table[data[self.RESPONSE_TABLE_MODE]][self.RESPONSE_TABLE_PIN_DATA_VALUE]
            self.analog_response_table[data[self.RESPONSE_TABLE_MODE]][self.RESPONSE_TABLE_PIN_DATA_VALUE] \
                = (data[self.MSB] << 7) + data[self.LSB]
            pin = data[0]
            pin_response_data_data = self.analog_response_table[pin]
            value = pin_response_data_data[self.RESPONSE_TABLE_PIN_DATA_VALUE]
            # check to see if there is a callback function attached to this pin
            callback = self.analog_response_table[data[self.RESPONSE_TABLE_MODE]][self.RESPONSE_TABLE_CALLBACK]
            # send the pin mode, pin number, and current data value
            if callback is not None:
                if value != previous_value:
                    # has the value changed since the last report
                    callback([self.pymata.ANALOG, pin, value])

            # check if data is to be latched
            # get the analog latching table entry for this pin
            latching_entry = self.analog_latch_table[pin]
            if latching_entry[self.LATCH_STATE] == self.LATCH_ARMED:
                # Has the latching criteria been met
                if latching_entry[self.LATCHED_THRESHOLD_TYPE] == self.ANALOG_LATCH_GT:
                    if value > latching_entry[self.ANALOG_LATCH_DATA_TARGET]:
                        if latching_entry[self.ANALOG_LATCH_CALLBACK] is not None:
                            self.analog_latch_table[pin] = [0, 0, 0, 0, 0, None]
                            latching_entry[self.ANALOG_LATCH_CALLBACK]([self.pymata.ANALOG | self.pymata.LATCH_MODE,
                                                                        pin, value, time.time()])
                        else:
                            updated_latch_entry = latching_entry
                            updated_latch_entry[self.LATCH_STATE] = self.LATCH_LATCHED
                            updated_latch_entry[self.ANALOG_LATCHED_DATA] = value
                            # time stamp it
                            updated_latch_entry[self.ANALOG_TIME_STAMP] = time.time()
                            self.analog_latch_table[pin] = updated_latch_entry
                    else:
                        pass  # haven't hit target
                elif latching_entry[self.LATCHED_THRESHOLD_TYPE] == self.ANALOG_LATCH_GTE:
                    if value >= latching_entry[self.ANALOG_LATCH_DATA_TARGET]:
                        if latching_entry[self.ANALOG_LATCH_CALLBACK] is not None:
                            self.analog_latch_table[pin] = [0, 0, 0, 0, 0, None]
                            latching_entry[self.ANALOG_LATCH_CALLBACK]([self.pymata.ANALOG | self.pymata.LATCH_MODE,
                                                                        pin, value, time.time()])
                        else:
                            updated_latch_entry = latching_entry
                            updated_latch_entry[self.LATCH_STATE] = self.LATCH_LATCHED
                            updated_latch_entry[self.ANALOG_LATCHED_DATA] = value
                            # time stamp it
                            updated_latch_entry[self.ANALOG_TIME_STAMP] = time.time()
                            self.analog_latch_table[pin] = updated_latch_entry
                    else:
                        pass  # haven't hit target:
                elif latching_entry[self.LATCHED_THRESHOLD_TYPE] == self.ANALOG_LATCH_LT:
                    if value < latching_entry[self.ANALOG_LATCH_DATA_TARGET]:
                        if latching_entry[self.ANALOG_LATCH_CALLBACK] is not None:
                            latching_entry[self.ANALOG_LATCH_CALLBACK]([self.pymata.ANALOG | self.pymata.LATCH_MODE,
                                                                        pin, value, time.time()])
                            self.analog_latch_table[pin] = [0, 0, 0, 0, 0, None]
                        else:
                            updated_latch_entry = latching_entry
                            updated_latch_entry[self.LATCH_STATE] = self.LATCH_LATCHED
                            updated_latch_entry[self.ANALOG_LATCHED_DATA] = value
                            # time stamp it
                            updated_latch_entry[self.ANALOG_TIME_STAMP] = time.time()
                            self.analog_latch_table[pin] = updated_latch_entry
                    else:
                        pass  # haven't hit target:
                elif latching_entry[self.LATCHED_THRESHOLD_TYPE] == self.ANALOG_LATCH_LTE:
                    if value <= latching_entry[self.ANALOG_LATCH_DATA_TARGET]:
                        if latching_entry[self.ANALOG_LATCH_CALLBACK] is not None:
                            latching_entry[self.ANALOG_LATCH_CALLBACK]([self.pymata.ANALOG | self.pymata.LATCH_MODE,
                                                                        pin, value, time.time()])
                            self.analog_latch_table[pin] = [0, 0, 0, 0, 0, None]
                        else:
                            updated_latch_entry = latching_entry
                            updated_latch_entry[self.LATCH_STATE] = self.LATCH_LATCHED
                            updated_latch_entry[self.ANALOG_LATCHED_DATA] = value
                            # time stamp it
                            updated_latch_entry[self.ANALOG_TIME_STAMP] = time.time()
                            self.analog_latch_table[pin] = updated_latch_entry
                    else:
                        pass  # haven't hit target:
                else:
                    pass