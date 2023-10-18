def command_handle(self):
        """Get the number of the shell command."""
        self.__results = self.execute(self.args.command)
        self.close()

        self.logger.debug("results: {}".format(self.__results))
        if not self.__results:
            self.unknown("{} return nothing.".format(self.args.command))
        if len(self.__results) != 1:
            self.unknown(
                "{} return more than one number.".format(
                    self.args.command))
        self.__result = int(self.__results[0])
        self.logger.debug("result: {}".format(self.__result))
        if not isinstance(self.__result, (int, long)):
            self.unknown(
                "{} didn't return single number.".format(
                    self.args.command))

        status = self.ok
        # Compare the vlaue.
        if self.__result > self.args.warning:
            status = self.warning
        if self.__result > self.args.critical:
            status = self.critical

        # Output
        self.shortoutput = "{0} return {1}.".format(
            self.args.command, self.__result)
        [self.longoutput.append(line)
         for line in self.__results if self.__results]
        self.perfdata.append("{command}={result};{warn};{crit};0;".format(
            crit=self.args.critical,
            warn=self.args.warning,
            result=self.__result,
            command=self.args.command))

        # Return status with message to Nagios.
        status(self.output(long_output_limit=None))
        self.logger.debug("Return status and exit to Nagios.")