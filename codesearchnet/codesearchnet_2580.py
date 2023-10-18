def add_arguments(parser):
  '''
  :param parser:
  :return:
  '''
  parser.add_argument(
      '--tracker_url',
      metavar='(a url; path to tracker; default: "' + consts.DEFAULT_TRACKER_URL + '")',
      default=consts.DEFAULT_TRACKER_URL)

  parser.add_argument(
      '--address',
      metavar='(an string; address to listen; default: "' + consts.DEFAULT_ADDRESS + '")',
      default=consts.DEFAULT_ADDRESS)

  parser.add_argument(
      '--port',
      metavar='(an integer; port to listen; default: ' + str(consts.DEFAULT_PORT) + ')',
      type=int,
      default=consts.DEFAULT_PORT)

  parser.add_argument(
      '--base_url',
      metavar='(a string; the base url path if operating behind proxy; default: '
      + str(consts.DEFAULT_BASE_URL) + ')',
      default=consts.DEFAULT_BASE_URL)

  return parser