def _get_deps_list(abs_path_to_pex):
  """Get a list of paths to included dependencies in the specified pex file

  Note that dependencies are located under `.deps` directory
  """
  pex = zipfile.ZipFile(abs_path_to_pex, mode='r')
  deps = list(set([re.match(egg_regex, i).group(1) for i in pex.namelist()
                   if re.match(egg_regex, i) is not None]))
  return deps