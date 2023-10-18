def process_top_line(self, words):
    """
    Process the line starting with "top"
    Example log:   top - 00:00:02 up 32 days,  7:08, 19 users,  load average: 0.00, 0.00, 0.00
    """
    self.ts_time = words[2]
    self.ts = self.ts_date + ' ' + self.ts_time
    self.ts = ts = naarad.utils.get_standardized_timestamp(self.ts, None)

    if self.ts_out_of_range(self.ts):
      self.ts_valid_lines = False
    else:
      self.ts_valid_lines = True
    up_days = int(words[4])
    up_hour_minute = words[6].split(':')  # E.g. '4:02,'
    up_minutes = int(up_hour_minute[0]) * 60 + int(up_hour_minute[1].split(',')[0])
    uptime_minute = up_days * 24 * 60 + up_minutes  # Converting days to minutes

    values = {}
    values['uptime_minute'] = str(uptime_minute)
    values['num_users'] = words[7]
    values['load_aver_1_minute'] = words[11][:-1]
    values['load_aver_5_minute'] = words[12][:-1]
    values['load_aver_15_minute'] = words[13]
    self.put_values_into_data(values)