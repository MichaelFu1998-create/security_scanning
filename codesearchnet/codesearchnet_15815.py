def read_csv(csv_name):
  """
  Read data from a csv file into a dictionary.
  :param str csv_name: path to a csv file.
  :return dict: a dictionary represents the data in file.
  """
  data = {}
  if not isinstance(csv_name, (str, unicode)):
    raise exceptions.InvalidDataFormat('luminol.utils: csv_name has to be a string!')
  with open(csv_name, 'r') as csv_data:
    reader = csv.reader(csv_data, delimiter=',', quotechar='|')
    for row in reader:
      try:
        key = to_epoch(row[0])
        value = float(row[1])
        data[key] = value
      except ValueError:
        pass
  return data