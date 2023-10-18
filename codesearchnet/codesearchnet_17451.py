def windowuptime(self, window_name):
        """
        Get window uptime

        @param window_name: Window name to look for, either full name,
        LDTP's name convention, or a Unix glob.
        @type window_name: string
    
        @return: "starttime, endtime" as datetime python object
        """
        tmp_time = self._remote_windowuptime(window_name)
        if tmp_time:
            tmp_time = tmp_time.split('-')
            start_time = tmp_time[0].split(' ')
            end_time = tmp_time[1].split(' ')
            _start_time = datetime.datetime(int(start_time[0]), int(start_time[1]),
                                            int(start_time[2]), int(start_time[3]),
                                            int(start_time[4]), int(start_time[5]))
            _end_time = datetime.datetime(int(end_time[0]), int(end_time[1]),
                                          int(end_time[2]), int(end_time[3]),
                                          int(end_time[4]), int(end_time[5]))
            return _start_time, _end_time
        return None