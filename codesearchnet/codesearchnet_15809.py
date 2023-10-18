def parse(self):
    """
    Parse the top output file
    Return status of the metric parse

    The raw log file is like the following:
    2014-06-23
    top - 00:00:02 up 18 days,  7:08, 19 users,  load average: 0.05, 0.03, 0.00
    Tasks: 447 total,   1 running, 443 sleeping,   2 stopped,   1 zombie
    Cpu(s):  1.6%us,  0.5%sy,  0.0%ni, 97.9%id,  0.0%wa,  0.0%hi,  0.0%si,  0.0%st
    Mem:    62.841G total,   15.167G used,   47.675G free,  643.434M buffers
    Swap:   63.998G total,    0.000k used,   63.998G free,   11.324G cached

    PID USER      PR  NI  VIRT  RES  SHR S %CPU %MEM    TIME+  COMMAND
    1730 root      20   0 4457m  10m 3328 S  1.9  0.0  80:13.45 lwregd
    The log lines can be generated by echo $t >> $RESULT/top.out &; top -b -n $COUNT -d $INTERVAL | grep -A 40 '^top' >> $RESULT/top.out &
    """

    for infile in self.infile_list:
      logger.info('Processing : %s', infile)
      status = True
      file_status = naarad.utils.is_valid_file(infile)
      if not file_status:
        return False

      with open(infile) as fh:
        for line in fh:
          words = line.split()
          if not words:
            continue

          # Pattern matches line of '2014-02-03'
          if re.match('^\d\d\d\d-\d\d-\d\d$', line):
            self.ts_date = words[0]
            continue

          prefix_word = words[0].strip()
          if prefix_word == 'top':
            self.process_top_line(words)
            self.saw_pid = False  # Turn off the processing of individual process line
          elif self.ts_valid_lines:
            if prefix_word == 'Tasks:':
              self.process_tasks_line(words)
            elif prefix_word == 'Cpu(s):':
              self.process_cpu_line(words)
            elif prefix_word == 'Mem:':
              self.process_mem_line(words)
            elif prefix_word == 'Swap:':
              self.process_swap_line(words)
            elif prefix_word == 'PID':
              self.saw_pid = True  # Turn on the processing of individual process line
              self.process_headers = words
            else:  # Each individual process line
              if self.saw_pid and len(words) >= len(self.process_headers):  # Only valid process lines
                self.process_individual_command(words)

    # Putting data in csv files;
    for out_csv in self.data.keys():    # All sub_metrics
      self.csv_files.append(out_csv)
      with open(out_csv, 'w') as fh:
        fh.write('\n'.join(self.data[out_csv]))

    gc.collect()
    return status