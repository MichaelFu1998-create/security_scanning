def run(self):
        """
        Open a connection over the serial line and receive data lines
        """
        if not self.device:
            return
        try:
            data = ""
            while (self.do_run):
                try:
                    if (self.device.inWaiting() > 1):
                        l = self.device.readline()[:-2]
                        l = l.decode("UTF-8")

                        if (l == "["):
                            # start recording
                            data = "["
                        elif (l == "]") and (len(data) > 4) and (data[0] == "["):
                            # now parse the input
                            data = data + "]"
                            self.store.register_json(data)
                            self.age()
                        elif (l[0:3] == "  {"):
                            # this is a data line
                            data = data + " " + l
                    else:
                        # this is a slow interface - give it some time
                        sleep(1)
                        # then count down..
                        self.age()
                except (UnicodeDecodeError, ValueError):
                    # only accepting unicode: throw away the whole bunch
                    data = ""
                    # and count down the exit condition
                    self.age()

        except serial.serialutil.SerialException:
            print("Could not connect to the serial line at " + self.device_name)