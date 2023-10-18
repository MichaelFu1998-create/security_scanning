def run(self):
        """
        This method starts the thread that continuously runs to receive and interpret
        messages coming from Firmata. This must be the last method in this file
        It also checks the deque for messages to be sent to Firmata.
        """
        # To add a command to the command dispatch table, append here.
        self.command_dispatch.update({self.REPORT_VERSION: [self.report_version, 2]})
        self.command_dispatch.update({self.REPORT_FIRMWARE: [self.report_firmware, 1]})
        self.command_dispatch.update({self.ANALOG_MESSAGE: [self.analog_message, 2]})
        self.command_dispatch.update({self.DIGITAL_MESSAGE: [self.digital_message, 2]})
        self.command_dispatch.update({self.ENCODER_DATA: [self.encoder_data, 3]})
        self.command_dispatch.update({self.SONAR_DATA: [self.sonar_data, 3]})
        self.command_dispatch.update({self.STRING_DATA: [self._string_data, 2]})
        self.command_dispatch.update({self.I2C_REPLY: [self.i2c_reply, 2]})
        self.command_dispatch.update({self.CAPABILITY_RESPONSE: [self.capability_response, 2]})
        self.command_dispatch.update({self.PIN_STATE_RESPONSE: [self.pin_state_response, 2]})
        self.command_dispatch.update({self.ANALOG_MAPPING_RESPONSE: [self.analog_mapping_response, 2]})
        self.command_dispatch.update({self.STEPPER_DATA: [self.stepper_version_response, 2]})

        while not self.is_stopped():
            if len(self.pymata.command_deque):
                # get next byte from the deque and process it
                data = self.pymata.command_deque.popleft()

                # this list will be populated with the received data for the command
                command_data = []

                # process sysex commands
                if data == self.START_SYSEX:
                    # next char is the actual sysex command
                    # wait until we can get data from the deque
                    while len(self.pymata.command_deque) == 0:
                        pass
                    sysex_command = self.pymata.command_deque.popleft()
                    # retrieve the associated command_dispatch entry for this command
                    dispatch_entry = self.command_dispatch.get(sysex_command)

                    # get a "pointer" to the method that will process this command
                    method = dispatch_entry[0]

                    # now get the rest of the data excluding the END_SYSEX byte
                    end_of_sysex = False
                    while not end_of_sysex:
                        # wait for more data to arrive
                        while len(self.pymata.command_deque) == 0:
                            pass
                        data = self.pymata.command_deque.popleft()
                        if data != self.END_SYSEX:
                            command_data.append(data)
                        else:
                            end_of_sysex = True

                            # invoke the method to process the command
                            method(command_data)
                            # go to the beginning of the loop to process the next command
                    continue

                # is this a command byte in the range of 0x80-0xff - these are the non-sysex messages

                elif 0x80 <= data <= 0xff:
                    # look up the method for the command in the command dispatch table
                    # for the digital reporting the command value is modified with port number
                    # the handler needs the port to properly process, so decode that from the command and
                    # place in command_data
                    if 0x90 <= data <= 0x9f:
                        port = data & 0xf
                        command_data.append(port)
                        data = 0x90
                    # the pin number for analog data is embedded in the command so, decode it
                    elif 0xe0 <= data <= 0xef:
                        pin = data & 0xf
                        command_data.append(pin)
                        data = 0xe0
                    else:
                        pass

                    dispatch_entry = self.command_dispatch.get(data)

                    # this calls the method retrieved from the dispatch table
                    method = dispatch_entry[0]

                    # get the number of parameters that this command provides
                    num_args = dispatch_entry[1]

                    # look at the number of args that the selected method requires
                    # now get that number of bytes to pass to the called method
                    for i in range(num_args):
                        while len(self.pymata.command_deque) == 0:
                            pass
                        data = self.pymata.command_deque.popleft()
                        command_data.append(data)
                        # go execute the command with the argument list
                    method(command_data)

                    # go to the beginning of the loop to process the next command
                    continue
            else:
                time.sleep(.1)