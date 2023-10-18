def make_tarfile(output_filename, source_dir):
  '''
  Tar a directory
  '''
  with tarfile.open(output_filename, "w:gz") as tar:
    tar.add(source_dir, arcname=os.path.basename(source_dir))