def prepare_output(self, row):
    """Convert types of task fields."""
    date_fields = ['last-update', 'create-time', 'start-time', 'end-time']
    int_fields = ['task-attempt']

    for col in date_fields:
      if col in row:
        row[col] = self.default_format_date(row[col])

    for col in int_fields:
      if col in row and row[col] is not None:
        row[col] = int(row[col])

    return row