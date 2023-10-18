def process_individual_command(self, words):
    """
    process the individual lines like this:
    #PID USER      PR  NI  VIRT  RES  SHR S %CPU %MEM    TIME+  COMMAND
    29303 root      20   0 35300 2580 1664 R  3.9  0.0   0:00.02 top
    11 root      RT   0     0    0    0 S  1.9  0.0   0:18.87 migration/2
    3702 root      20   0 34884 4192 1692 S  1.9  0.0  31:40.47 cf-serverd
    It does not record all processes due to memory concern; rather only records interested processes (based on user input of PID and COMMAND)
    """
    pid_index = self.process_headers.index('PID')
    proces_index = self.process_headers.index('COMMAND')

    pid = words[pid_index]
    process = words[proces_index]
    if pid in self.PID or process in self.COMMAND:
      process_name = process.split('/')[0]

      values = {}
      for word_col in self.process_headers:
        word_index = self.process_headers.index(word_col)
        if word_col in ['VIRT', 'RES', 'SHR']:  # These values need to convert to 'G'
          values[process_name + '_' + pid + '_' + word_col] = self.convert_to_G(words[word_index])
        elif word_col in ['PR', 'NI', '%CPU', '%MEM']:  # These values will be assigned later or ignored
          values[process_name + '_' + pid + '_' + word_col.strip('%')] = words[word_index]

        uptime_index = self.process_headers.index('TIME+')
        uptime = words[uptime_index].split(':')
        uptime_sec = float(uptime[0]) * 60 + float(uptime[1])
        values[process_name + '_' + pid + '_' + 'TIME'] = str(uptime_sec)
      self.put_values_into_data(values)