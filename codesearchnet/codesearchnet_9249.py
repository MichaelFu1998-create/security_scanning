def stdout(self):
        """
        Converts stdout string to a list.
        """
        if self._streaming:
            stdout = []
            while not self.__stdout.empty():
                try:
                    line = self.__stdout.get_nowait()
                    stdout.append(line)
                except:
                    pass
        else:
            stdout =  self.__stdout
        return stdout