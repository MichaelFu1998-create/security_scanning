def write(self, data):
        """
            write the data to the serial port
            return: None
        """
        if sys.version_info[0] < 3:
            self.arduino.write(data)
        else:
            self.arduino.write(bytes([ord(data)]))