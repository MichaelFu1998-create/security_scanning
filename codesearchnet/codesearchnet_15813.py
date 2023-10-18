def download_url_single(inputs, outdir, outfile=None):
  """
  Downloads a http(s) url to a local file
  :param str inputs:  the absolute url
  :param str outdir: Required. the local directory to put the downloadedfiles.
  :param str outfile: // Optional. If this is given, the downloaded url will be renated to outfile;
    If this is not given, then the local file will be the original one, as given in url.
  :return: the local full path name of downloaded url
  """

  if not inputs or type(inputs) != str or not outdir or type(outdir) != str:
    logging.error("The call parameters are invalid.")
    return
  else:
    if not os.path.exists(outdir):
      os.makedirs(outdir)

  output_file = handle_single_url(inputs, outdir, outfile)
  return output_file