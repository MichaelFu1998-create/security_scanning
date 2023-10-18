def find_address_file(self):
        """
        Finds the OMXPlayer DBus connection
        Assumes there is an alive OMXPlayer process.
        :return:
        """
        possible_address_files = []
        while not possible_address_files:
            # filter is used here as glob doesn't support regexp :(
            isnt_pid_file = lambda path: not path.endswith('.pid')
            possible_address_files = list(filter(isnt_pid_file,
                                            glob('/tmp/omxplayerdbus.*')))
            possible_address_files.sort(key=lambda path: os.path.getmtime(path))
            time.sleep(0.05)

        self.path = possible_address_files[-1]