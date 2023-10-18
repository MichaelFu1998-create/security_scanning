def __get_current_datetime(self):
        """Get current datetime for every file."""
        self.wql_time = "SELECT LocalDateTime FROM Win32_OperatingSystem"
        self.current_time = self.query(self.wql_time)
        # [{'LocalDateTime': '20160824161431.977000+480'}]'
        self.current_time_string = str(
            self.current_time[0].get('LocalDateTime').split('.')[0])
        # '20160824161431'
        self.current_time_format = datetime.datetime.strptime(
            self.current_time_string, '%Y%m%d%H%M%S')
        # param: datetime.datetime(2016, 8, 24, 16, 14, 31) -> type:
        # datetime.datetime
        return self.current_time_format