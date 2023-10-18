def filenumber_handle(self):
        """Get the number of file in the folder."""
        self.file_list = []
        self.count = 0
        status = self.ok

        if self.args.recursion:
            self.__result, self.__file_list = self.__get_folder(self.args.path)
        else:
            self.__result, self.__file_list = self.__get_file(self.args.path)

        # Compare the vlaue.
        if self.__result > self.args.critical:
            status = self.critical
        elif self.__result > self.args.warning:
            status = self.warning
        else:
            status = self.ok

        # Output
        self.shortoutput = "Found {0} files in {1}.".format(self.__result,
                                                            self.args.path)
        self.logger.debug("file_list: {}".format(self.__file_list))
        [self.longoutput.append(file_data.get('Name'))
         for file_data in self.__file_list]
        self.perfdata.append("{path}={result};{warn};{crit};0;".format(
            crit=self.args.critical,
            warn=self.args.warning,
            result=self.__result,
            path=self.args.path))

        # Return status with message to Nagios.
        status(self.output(long_output_limit=None))
        self.logger.debug("Return status and exit to Nagios.")