def add(reader, writer, column, start, stop, value):
  """Adds a value over a range of rows.

  Args:
    reader: A FileRecordStream object with input data.
    writer: A FileRecordStream object to write output data to.
    column: The column of data to modify.
    start: The first row in the range to modify.
    end: The last row in the range to modify.
    value: The value to add.
  """
  for i, row in enumerate(reader):
    if i >= start and i <= stop:
      row[column] = type(value)(row[column]) + value
    writer.appendRecord(row)