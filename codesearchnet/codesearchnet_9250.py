def stderr(self):
        """
        Converts stderr string to a list.
        """
        if self._streaming:
            stderr = []
            while not self.__stderr.empty():
                try:
                    line = self.__stderr.get_nowait()
                    stderr.append(line)
                except:
                    pass
        else:
            stderr = self.__stderr
        return stderr