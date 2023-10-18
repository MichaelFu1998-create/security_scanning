def collect(self):
    """
    Take a list of metrics, filter all metrics based on hostname, and metric_type
    For each metric, merge the corresponding csv files into one,update corresponding properties such as csv_column_map.
    Users can specify functions: raw, count (qps), sum (aggregated value), avg (averaged value)
    The timestamp granularity of aggregated submetrics is in seconds (sub-second is not supported)
    """

    for aggr_metric in self.aggr_metrics:   # e.g., SAR-device.sda.await:count,sum,avg
      functions_aggr = []
      fields = aggr_metric.split(":")
      cur_metric_type = fields[0].split(".")[0]  # e.g. SAR-device

      if len(fields) > 1:  # The user has to specify the aggregate functions (i.e., :raw,count,sum,avg)
        func_user = ''.join(fields[1].split())
        functions_aggr.extend(func_user.split(","))
      else:  # no user input of aggregate functions
        return True

      cur_column = '.'.join(fields[0].split('.')[1:])    # e.g. sda.await or all.percent-sys

      # Store data points of various aggregation functions
      aggr_data = {}
      aggr_data['raw'] = []   # Store all the raw values
      aggr_data['sum'] = defaultdict(float)   # Store the sum values for each timestamp
      aggr_data['count'] = defaultdict(int)  # Store the count of each timestamp (i.e. qps)

      for metric in self.metrics:   # Loop the list to find from all metrics to merge
        if metric.hostname in self.aggr_hosts and \
           cur_column in metric.csv_column_map.values():
          file_csv = metric.get_csv(cur_column)
          timestamp_format = None
          with open(file_csv) as fh:
            for line in fh:
              aggr_data['raw'].append(line.rstrip())
              words = line.split(",")
              ts = words[0].split('.')[0]   # In case of sub-seconds; we only want the value of seconds;
              if not timestamp_format or timestamp_format == 'unknown':
                timestamp_format = naarad.utils.detect_timestamp_format(ts)
              if timestamp_format == 'unknown':
                continue
              ts = naarad.utils.get_standardized_timestamp(ts, timestamp_format)
              aggr_data['sum'][ts] += float(words[1])
              aggr_data['count'][ts] += 1
      # "raw" csv file
      if 'raw' in functions_aggr:
        out_csv = self.get_csv(cur_column, 'raw')
        self.csv_files.append(out_csv)
        with open(out_csv, 'w') as fh:
          fh.write("\n".join(sorted(aggr_data['raw'])))

      # "sum"  csv file
      if 'sum' in functions_aggr:
        out_csv = self.get_csv(cur_column, 'sum')
        self.csv_files.append(out_csv)
        with open(out_csv, 'w') as fh:
          for (k, v) in sorted(aggr_data['sum'].items()):
            fh.write(k + "," + str(v) + '\n')

      # "avg" csv file
      if 'avg' in functions_aggr:
        out_csv = self.get_csv(cur_column, 'avg')
        self.csv_files.append(out_csv)
        with open(out_csv, 'w') as fh:
          for (k, v) in sorted(aggr_data['sum'].items()):
            fh.write(k + "," + str(v / aggr_data['count'][k]) + '\n')

      # "count" csv file (qps)
      if 'count' in functions_aggr:
        out_csv = self.get_csv(cur_column, 'count')
        self.csv_files.append(out_csv)
        with open(out_csv, 'w') as fh:
          for (k, v) in sorted(aggr_data['count'].items()):
            fh.write(k + "," + str(v) + '\n')

      gc.collect()
    return True