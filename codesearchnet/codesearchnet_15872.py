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
    cur_zone = None
    cur_submetric = None
    cur_value = None
    data = {}  # stores the data of each column
    for input_file in self.infile_list:
      logger.info('Processing : %s', input_file)
      timestamp_format = None
      with open(input_file) as fh:
        for line in fh:
          words = line.replace(',', ' ').split()           # [0] is day; [1] is seconds; [2...] is field names:;
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
          if words[2] == 'Node':  # Node 0 zone      DMA
            cols = words[2:]
            cur_zone = '.'.join(cols)
            continue
          elif words[2] == 'pages':  # pages free     3936
            cur_submetric = words[2] + '.' + words[3]  # pages.free
            cur_value = words[4]
          elif words[2] in self.processed_sub_metrics:
            cur_submetric = 'pages' + '.' + words[2]  # pages.min
            cur_value = words[3]
          elif words[2] in self.skipped_sub_metrics:
            continue
          else:   # other useful submetrics
            cur_submetric = words[2]
            cur_value = words[3]
          col = cur_zone + '.' + cur_submetric  # prefix with 'Node.0.zone.DMA.
          # only process zones specified in config
          if cur_zone and self.zones and cur_zone not in self.zones:
            continue
          self.sub_metric_unit[col] = 'pages'  # The unit of the sub metric. For /proc/zoneinfo, they are all in pages
          # only process sub_metrics specified in config.
          if self.sub_metrics and cur_submetric and cur_submetric not in self.sub_metrics:
            continue
          if col in self.column_csv_map:
            out_csv = self.column_csv_map[col]
          else:
            out_csv = self.get_csv(col)   # column_csv_map[] is assigned in get_csv()
            data[out_csv] = []
          data[out_csv].append(ts + "," + cur_value)
    # post processing, putting data in csv files;
    for csv in data.keys():
      self.csv_files.append(csv)
      with open(csv, 'w') as fh:
        fh.write('\n'.join(sorted(data[csv])))
    return status