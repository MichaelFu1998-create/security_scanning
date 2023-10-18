def get_urls_from_seed(url):
  """
  get a list of urls from a seeding url, return a list of urls

  :param str url: a full/absolute url, e.g. http://www.cnn.com/logs/
  :return: a list of full/absolute urls.
  """

  if not url or type(url) != str or not naarad.utils.is_valid_url(url):
    logger.error("get_urls_from_seed() does not have valid seeding url.")
    return

  # Extract the host info of "http://host:port/" in case of href urls are elative urls (e.g., /path/gc.log)
  # Then join (host info and relative urls) to form the complete urls
  base_index = url.find('/', len("https://"))   # get the first "/" after http://" or "https://"; handling both cases.
  base_url = url[:base_index]      # base_url = "http://host:port" or https://host:port" or http://host" (where no port is given)

  # Extract the "href" denoted urls
  urls = []
  try:
    response = urllib2.urlopen(url)
    hp = HTMLLinkExtractor()
    hp.feed(response.read())
    urls = hp.links
    hp.close()
  except urllib2.HTTPError:
    logger.error("Got HTTPError when opening the url of %s" % url)
    return urls

  # Check whether the url is relative or complete
  for i in range(len(urls)):
    if not urls[i].startswith("http://") and not urls[i].startswith("https://"):    # a relative url ?
      urls[i] = base_url + urls[i]

  return urls