def fileage_handle(self):
        """Get the number of file in the folder."""
        self.file_list = []
        self.ok_file = []
        self.warn_file = []
        self.crit_file = []
        status = self.ok

        if self.args.recursion:
            self.__file_list = self.__get_folder(self.args.path)
        else:
            self.__file_list = self.__get_file(self.args.path)
        self.logger.debug("file_list: {}".format(self.__file_list))
        # [{'LastModified': '20160824142017.737101+480', 'Name': 'd:\\test\\1.txt'},
        # {'LastModified': '20160824142021.392101+480', 'Name': 'd:\\test\\2.txt'},
        # {'LastModified': '20160824142106.460101+480', 'Name': 'd:\\test\\test1\\21.txt'}]

        for file_dict in self.__file_list:
            self.filename = file_dict.get('Name')
            if self.filename and self.filename != 'Name':
                self.logger.debug(
                    "===== start to compare {} =====".format(
                        self.filename))

                self.file_datetime_string = file_dict.get(
                    'LastModified').split('.')[0]
                self.file_datetime = datetime.datetime.strptime(
                    self.file_datetime_string, '%Y%m%d%H%M%S')
                self.logger.debug(
                    "file_datetime: {}".format(
                        self.file_datetime))

                self.current_datetime = self.__get_current_datetime()
                self.logger.debug(
                    "current_datetime: {}".format(
                        self.current_datetime))

                self.__delta_datetime = self.current_datetime - self.file_datetime
                self.logger.debug(
                    "delta_datetime: {}".format(
                        self.__delta_datetime))
                self.logger.debug(
                    "warn_datetime: {}".format(
                        datetime.timedelta(
                            minutes=self.args.warning)))
                self.logger.debug(
                    "crit_datetime: {}".format(
                        datetime.timedelta(
                            minutes=self.args.critical)))
                if self.__delta_datetime > datetime.timedelta(
                        minutes=self.args.critical):
                    self.crit_file.append(self.filename)
                elif self.__delta_datetime > datetime.timedelta(minutes=self.args.warning):
                    self.warn_file.append(self.filename)
                else:
                    self.ok_file.append(self.filename)

        # Compare the vlaue.
        if self.crit_file:
            status = self.critical
        elif self.warn_file:
            status = self.warning
        else:
            status = self.ok

        # Output
        self.shortoutput = "Found {0} files out of date.".format(
            len(self.crit_file))
        if self.crit_file:
            self.longoutput.append("===== Critical File out of date ====")
        [self.longoutput.append(filename)
         for filename in self.crit_file if self.crit_file]
        if self.warn_file:
            self.longoutput.append("===== Warning File out of date ====")
        [self.longoutput.append(filename)
         for filename in self.warn_file if self.warn_file]
        if self.ok_file:
            self.longoutput.append("===== OK File out of date ====")
        [self.longoutput.append(filename)
         for filename in self.ok_file if self.ok_file]
        self.perfdata.append("{path}={result};{warn};{crit};0;".format(
            crit=self.args.critical,
            warn=self.args.warning,
            result=len(self.crit_file),
            path=self.args.drive + self.args.path))

        # Return status with message to Nagios.
        status(self.output(long_output_limit=None))
        self.logger.debug("Return status and exit to Nagios.")