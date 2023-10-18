def define_options(address, port, tracker_url, base_url):
  '''
  :param address:
  :param port:
  :param tracker_url:
  :return:
  '''
  define("address", default=address)
  define("port", default=port)
  define("tracker_url", default=tracker_url)
  define("base_url", default=base_url)