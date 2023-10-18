def put_values_into_data(self, values):
    """
    Take the (col, value) in 'values', append value into 'col' in self.data[]
    """
    for col, value in values.items():
      if col in self.column_csv_map:
        out_csv = self.column_csv_map[col]
      else:
        out_csv = self.get_csv(col)   # column_csv_map[] is assigned in get_csv()
        self.data[out_csv] = []
      self.data[out_csv].append(self.ts + "," + value)