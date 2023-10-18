def filter_spouts(table, header):
  """ filter to keep spouts """
  spouts_info = []
  for row in table:
    if row[0] == 'spout':
      spouts_info.append(row)
  return spouts_info, header