def create_tar(tar_filename, files, config_dir, config_files):
  '''
  Create a tar file with a given set of files
  '''
  with contextlib.closing(tarfile.open(tar_filename, 'w:gz', dereference=True)) as tar:
    for filename in files:
      if os.path.isfile(filename):
        tar.add(filename, arcname=os.path.basename(filename))
      else:
        raise Exception("%s is not an existing file" % filename)

    if os.path.isdir(config_dir):
      tar.add(config_dir, arcname=get_heron_sandbox_conf_dir())
    else:
      raise Exception("%s is not an existing directory" % config_dir)

    for filename in config_files:
      if os.path.isfile(filename):
        arcfile = os.path.join(get_heron_sandbox_conf_dir(), os.path.basename(filename))
        tar.add(filename, arcname=arcfile)
      else:
        raise Exception("%s is not an existing file" % filename)