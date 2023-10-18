def parse_innotop_mode_b(self):
    """ Generic parsing method for all other modes """
    with open(self.infile, 'r') as infh:
      # Pre processing to figure out different headers
      max_row_quot = 0
      valrow = -1
      thisrowcolumns = {}
      data = {}
      while True:
        line1 = infh.readline()
        words = line1.split()
        # special case for -I (iostat) option
        # skipping all the 'thread' lines
        if words[1] == "thread" and self.metric_type == "INNOTOP-I":
          while True:
            line1 = infh.readline()
            words = line1.split()
            if naarad.utils.is_number(words[1]):
              line1 = infh.readline()
            else:
              break
        if words[1] == "thread" and self.metric_type == "INNOTOP-R":
          break
        # Skip next line
        infh.readline()
        last_ts = words[0].strip().replace('T', ' ')
        if not naarad.utils.is_number(words[1]):
          thisrowcolumns[max_row_quot] = words[1:]
          for column in words[1:]:
            if self.options and column not in self.options:
              continue
            data[column] = []
          if self.metric_type == "INNOTOP-I":
            data["check_pt_age"] = []
          max_row_quot += 1
        else:
          break
      # infh.seek(0)
      # Real Processing
      for line in infh:
        l = line.strip().split(' ', 1)
        if len(l) <= 1:
          continue
        ts = l[0].strip().replace('T', ' ')
        if not ts == last_ts:
          last_ts = ts
          valrow = -1
        try:
          words = l[1].strip().split('\t')
        except IndexError:
          logger.warn("Bad line: %s", line)
          continue
        # special case for -I (iostat) option
        # skipping all the 'thread' lines
        if words[0] == "thread" or (naarad.utils.is_number(words[0]) and "thread" in words[1]):
          continue
        if naarad.utils.is_number(words[0]):
          valrow += 1
          quot = valrow % max_row_quot
          # Special case for -R, skipping all 'thread' value lines
          if quot >= len(thisrowcolumns):
            continue
          columns = thisrowcolumns[quot]
          if len(words) > len(columns):
            continue
          for i in range(len(words)):
            if self.options and columns[i] not in self.options:
              continue
            column = columns[i]
            # Converting -- to 0, seen this for buf_pool_hit_rate
            if words[i] == "--":
              words[i] = "0"
            ts = naarad.utils.reconcile_timezones(ts, self.timezone, self.graph_timezone)
            # Calculating check point age
            if self.metric_type == "INNOTOP-I":
              if column == "log_seq_no":
                log_seq_no = int(words[i])
              elif column == "log_flushed_to":
                check_pt_age = log_seq_no - int(words[i])
                tup = [ts, str(check_pt_age)]
                data["check_pt_age"].append(tup)
            tup = [ts, words[i]]
            data[column].append(tup)
    # Post Proc, writing the different out files
    for column in data:
      csvfile = self.get_csv(column)
      self.csv_files.append(csvfile)
      with open(csvfile, 'w') as outfh:
        for tup in data[column]:
          outfh.write(','.join(tup))
          outfh.write('\n')
    return True