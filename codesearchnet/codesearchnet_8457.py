def start(self):
        """Run FIO job in thread"""

        self.__thread = Threads(target=self.run, args=(True, True, False))
        self.__thread.setDaemon(True)
        self.__thread.start()