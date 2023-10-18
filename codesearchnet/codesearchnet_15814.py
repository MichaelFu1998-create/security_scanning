def download_url_regex(inputs, outdir, regex=".*"):
  """
  Downloads http(s) urls to a local files
  :param str inputs: Required, the seed url
  :param str outdir: Required. the local directory to put the downloadedfiles.
  :param str regex: Optional, a regex string. If not given, then all urls will be valid
  :return: A list of local full path names (downloaded from inputs)
  """
  if not inputs or type(inputs) != str \
     or not outdir or type(outdir) != str:
    logging.error("The call parameters are invalid.")
    return
  else:
    if not os.path.exists(outdir):
      os.makedirs(outdir)

  output_files = []
  files = get_urls_from_seed(inputs)
  for f in files:
    if re.compile(regex).match(f):
      output_file = handle_single_url(f, outdir)
      output_files.append(output_file)

  return output_files