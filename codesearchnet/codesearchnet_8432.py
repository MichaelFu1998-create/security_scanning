def start(self):
        """Start DMESG job in thread"""

        self.__thread = Thread(target=self.__run, args=(True, False))
        self.__thread.setDaemon(True)
        self.__thread.start()