def parse(self):
    """
    Parse the netstat output file
    :return: status of the metric parse
    """
    # sample netstat output: 2014-04-02 15:44:02.86612	tcp     9600      0 host1.localdomain.com.:21567 remote.remotedomain.com:51168 ESTABLISH pid/process
    data = {}  # stores the data of each sub-metric
    for infile in self.infile_list:
      logger.info('Processing : %s', infile)
      timestamp_format = None
      with open(infile) as fh:
        for line in fh:
          if 'ESTABLISHED' not in line:
            continue
          words = line.split()
          if len(words) < 8 or words[2] != 'tcp':
            continue
          ts = words[0] + " " + words[1]
          if not timestamp_format or timestamp_format == 'unknown':
            timestamp_format = naarad.utils.detect_timestamp_format(ts)
          if timestamp_format == 'unknown':
            continue
          ts = naarad.utils.get_standardized_timestamp(ts, timestamp_format)
          if self.ts_out_of_range(ts):
            continue
          # filtering based on user input; (local socket, remote socket, pid/process)
          local_end, remote_end, interested = self._check_connection(words[5], words[6], words[8])
          if interested:
            self._add_data_line(data, local_end + '.' + remote_end + '.RecvQ', words[3], ts)
            self._add_data_line(data, local_end + '.' + remote_end + '.SendQ', words[4], ts)
    # post processing, putting data in csv files;
    for csv in data.keys():
      self.csv_files.append(csv)
      with open(csv, 'w') as fh:
        fh.write('\n'.join(sorted(data[csv])))
    return True