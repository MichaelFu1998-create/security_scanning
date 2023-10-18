def get_standardized_timestamp(timestamp, ts_format):
  """
  Given a timestamp string, return a time stamp in the epoch ms format. If no date is present in
  timestamp then today's date will be added as a prefix before conversion to epoch ms
  """
  if not timestamp:
    return None
  if timestamp == 'now':
    timestamp = str(datetime.datetime.now())
  if not ts_format:
    ts_format = detect_timestamp_format(timestamp)
  try:
    if ts_format == 'unknown':
      logger.error('Unable to determine timestamp format for : %s', timestamp)
      return -1
    elif ts_format == 'epoch':
      ts = int(timestamp) * 1000
    elif ts_format == 'epoch_ms':
      ts = timestamp
    elif ts_format == 'epoch_fraction':
      ts = int(timestamp[:10]) * 1000 + int(timestamp[11:])
    elif ts_format in ('%H:%M:%S', '%H:%M:%S.%f'):
      date_today = str(datetime.date.today())
      dt_obj = datetime.datetime.strptime(date_today + ' ' + timestamp, '%Y-%m-%d ' + ts_format)
      ts = calendar.timegm(dt_obj.utctimetuple()) * 1000 + dt_obj.microsecond / 1000
    else:
      dt_obj = datetime.datetime.strptime(timestamp, ts_format)
      ts = calendar.timegm(dt_obj.utctimetuple()) * 1000 + dt_obj.microsecond / 1000
  except ValueError:
    return -1
  return str(ts)