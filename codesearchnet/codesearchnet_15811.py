def stream_url(url):
  """
  Read response of specified url into memory and return to caller. No persistence to disk.
  :return: response content if accessing the URL succeeds, False otherwise
  """
  try:
    response = urllib2.urlopen(url)
    response_content = response.read()
    return response_content
  except (urllib2.URLError, urllib2.HTTPError) as e:
    logger.error('Unable to access requested URL: %s', url)
    return False