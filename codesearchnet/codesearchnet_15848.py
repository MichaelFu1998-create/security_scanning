def parse(self):
    """
    Parse the vmstat file
    :return: status of the metric parse
    """
    file_status = True
    for input_file in self.infile_list:
      file_status = file_status and naarad.utils.is_valid_file(input_file)
      if not file_status:
        return False
    status = True
    data = {}  # stores the data of each column
    for input_file in self.infile_list:
      logger.info('Processing : %s', input_file)
      timestamp_format = None
      with open(input_file) as fh:
        for line in fh:
          words = line.split()        # [0] is day; [1] is seconds; [2] is field name:; [3] is value  [4] is unit
          if len(words) < 3:
            continue
          ts = words[0] + " " + words[1]
          if not timestamp_format or timestamp_format == 'unknown':
            timestamp_format = naarad.utils.detect_timestamp_format(ts)
          if timestamp_format == 'unknown':
            continue
          ts = naarad.utils.get_standardized_timestamp(ts, timestamp_format)
          if self.ts_out_of_range(ts):
            continue
          col = words[2].strip(':')
          # only process sub_metrics specified in config.
          if self.sub_metrics and col not in self.sub_metrics:
            continue
          # add unit to metric description; most of the metrics have 'KB'; a few others do not have unit, they are in number of pages
          if len(words) > 4 and words[4]:
            unit = words[4]
          else:
            unit = 'pages'
          self.sub_metric_unit[col] = unit
          # stores the values in data[] before finally writing out
          if col in self.column_csv_map:
            out_csv = self.column_csv_map[col]
          else:
            out_csv = self.get_csv(col)   # column_csv_map[] is assigned in get_csv()
            data[out_csv] = []
          data[out_csv].append(ts + "," + words[3])
    # post processing, putting data in csv files;
    for csv in data.keys():
      self.csv_files.append(csv)
      with open(csv, 'w') as fh:
        fh.write('\n'.join(sorted(data[csv])))
    return status