def add_tracker_url(parser):
  """ add optional tracker_url argument """
  parser.add_argument(
      '--tracker_url',
      metavar='(tracker url; default: "' + DEFAULT_TRACKER_URL + '")',
      type=str, default=DEFAULT_TRACKER_URL)
  return parser