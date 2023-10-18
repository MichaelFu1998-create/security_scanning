def is_valid_url(url):
  """
  Check if a given string is in the correct URL format or not

  :param str url:
  :return: True or False
  """
  regex = re.compile(r'^(?:http|ftp)s?://'
                     r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
                     r'localhost|'
                     r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
                     r'(?::\d+)?'
                     r'(?:/?|[/?]\S+)$', re.IGNORECASE)
  if regex.match(url):
    logger.info("URL given as config")
    return True
  else:
    return False