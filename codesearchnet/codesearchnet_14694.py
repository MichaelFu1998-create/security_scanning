def write_lines(self, data):
        """write lines, one by one, separated by \n to device"""
        lines = data.replace('\r', '').split('\n')
        for line in lines:
            self.__exchange(line)