def filter_bolts(table, header):
  """ filter to keep bolts """
  bolts_info = []
  for row in table:
    if row[0] == 'bolt':
      bolts_info.append(row)
  return bolts_info, header