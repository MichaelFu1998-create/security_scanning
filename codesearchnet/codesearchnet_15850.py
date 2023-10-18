def parse_innotop_mode_m(self):
    """ Special parsing method for Innotop "Replication Status" results (innotop --mode M)"""
    with open(self.infile, 'r') as infh:
      # Pre processing to figure out different headers
      max_row_quot = 0
      valrow = -1
      thisrowcolumns = {}
      data = {}
      last_ts = None
      while True:
        # 2012-05-11T00:00:02 master_host slave_sql_running  time_behind_master  slave_catchup_rate  slave_open_temp_tables  relay_log_pos   last_error
        line1 = infh.readline()
        words = line1.split()
        # Skip next line
        infh.readline()
        is_header = True
        for word in words:
          if naarad.utils.is_number(word):
            last_ts = words[0].strip().replace('T', ' ')
            is_header = False
            break  # from this loop
        if len(words) > 2 and is_header:
          thisrowcolumns[max_row_quot] = words[2:]
          for column in thisrowcolumns[max_row_quot]:
            data[column] = []
          max_row_quot += 1
        else:
          break
          # from pre-processing. All headers accounted for

      # Real Processing
      if not last_ts:
        logger.warn("last_ts not set, looks like there is no data in file %s", self.infile)
        return True
      infh.seek(0)
      is_bad_line = False
      outfilehandlers = {}
      for line in infh:
        l = line.strip().split(' ', 1)
        # Blank line
        if len(l) <= 1:
          continue
        ts = l[0].strip().replace('T', ' ')
        if ts != last_ts:
          last_ts = ts
          valrow = -1
        nameval = l[1].strip().split('\t', 1)
        try:
          words = nameval[1].split('\t')
        except IndexError:
          logger.warn("Bad line: %s", line)
          continue
        valrow += 1
        command = nameval[0]
        if command not in outfilehandlers:
          outfilehandlers[command] = {}
        quot = valrow % max_row_quot
        columns = thisrowcolumns[quot]
        for i in range(len(words)):
          if len(words) > len(columns):
            logger.warn("Mismatched number of columns: %s", line)
            logger.warn("%d %d", len(words), len(columns))
            break
          if words[i] in columns:
            logger.warn("Skipping line: %s", line)
            valrow -= 1
            break
          if self.options and columns[i] not in self.options:
            continue
          if columns[i] not in outfilehandlers[command]:
            outfilehandlers[command][columns[i]] = open(self.get_csv_C(command, columns[i]), 'w')
            self.csv_files.append(self.get_csv_C(command, columns[i]))
          ts = naarad.utils.reconcile_timezones(ts, self.timezone, self.graph_timezone)
          outfilehandlers[command][columns[i]].write(ts + ',')
          outfilehandlers[command][columns[i]].write(words[i])
          outfilehandlers[command][columns[i]].write('\n')
      for command in outfilehandlers:
        for column in outfilehandlers[command]:
          outfilehandlers[command][column].close()
    return True