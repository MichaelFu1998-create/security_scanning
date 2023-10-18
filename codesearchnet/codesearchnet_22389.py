def filenumber_handle(self):
        """Get the number of files in the folder."""
        self.__results = []
        self.__dirs = []
        self.__files = []
        self.__ftp = self.connect()
        self.__ftp.dir(self.args.path, self.__results.append)
        self.logger.debug("dir results: {}".format(self.__results))
        self.quit()

        status = self.ok

        for data in self.__results:
            if "<DIR>" in data:
                self.__dirs.append(str(data.split()[3]))
            else:
                self.__files.append(str(data.split()[2]))

        self.__result = len(self.__files)
        self.logger.debug("result: {}".format(self.__result))

        # Compare the vlaue.
        if self.__result > self.args.warning:
            status = self.warning
        if self.__result > self.args.critical:
            status = self.critical

        # Output
        self.shortoutput = "Found {0} files in {1}.".format(self.__result,
                                                            self.args.path)
        [self.longoutput.append(line)
         for line in self.__results if self.__results]
        self.perfdata.append("{path}={result};{warn};{crit};0;".format(
            crit=self.args.critical,
            warn=self.args.warning,
            result=self.__result,
            path=self.args.path))

        self.logger.debug("Return status and output.")
        status(self.output())