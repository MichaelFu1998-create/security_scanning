def handle_single_url(url, outdir, outfile=None):
  """
  Base function which takes a single url, download it to outdir/outfile
  :param str url: a full/absolute url, e.g. http://www.cnn.com/log.zip
  :param str outdir: the absolute local directory. e.g. /home/user1/tmp/
  :param str outfile: (optional) filename stored in local directory. If outfile is not given, extract the filename from url
  :return: the local full path name of downloaded url
  """
  if not url or type(url) != str \
     or not outdir or type(outdir) != str:
      logger.error('passed in parameters %s %s are incorrect.' % (url, outdir))
      return

  if not naarad.utils.is_valid_url(url):
    logger.error("passed in url %s is incorrect." % url)
    return

  if not outfile:
    segs = url.split('/')
    outfile = segs[-1]
    outfile = urllib2.quote(outfile)

  output_file = os.path.join(outdir, outfile)
  if os.path.exists(output_file):
    logger.warn("the %s already exists!" % outfile)

  with open(output_file, "w") as fh:
    try:
      response = urllib2.urlopen(url)
      fh.write(response.read())
    except urllib2.HTTPError:
      logger.error("got HTTPError when retrieving %s" % url)
      return
    except urllib2.URLError:
      logger.error("got URLError when retrieving %s" % url)
      return

  return output_file