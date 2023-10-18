def _add_data_line(self, data, col, value, ts):
    """
    Append the data point to the dictionary of "data"
    :param data: The dictionary containing all data
    :param col: The sub-metric name e.g. 'host1_port1.host2_port2.SendQ'
    :param value: integer
    :param ts: timestamp
    :return: None
    """
    if col in self.column_csv_map:
      out_csv = self.column_csv_map[col]
    else:
      out_csv = self.get_csv(col)   # column_csv_map[] is assigned in get_csv()
      data[out_csv] = []
    data[out_csv].append(ts + "," + value)