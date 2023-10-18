def maybe_download_and_extract():
  """Download and extract processed data and embeddings."""
  dest_directory = '.'
  filename = DATA_URL.split('/')[-1]
  filepath = os.path.join(dest_directory, filename)
  if not os.path.exists(filepath):
    def _progress(count, block_size, total_size):
      sys.stdout.write('\r>> Downloading %s %.1f%%' % (filename,
          float(count * block_size) / float(total_size) * 100.0))
      sys.stdout.flush()
    filepath, _ = urllib.request.urlretrieve(DATA_URL, filepath, _progress)
    print()
    statinfo = os.stat(filepath)
    print('Successfully downloaded', filename, statinfo.st_size, 'bytes.')
  extracted_dir_path = os.path.join(dest_directory, 'trees')
  if not os.path.exists(extracted_dir_path):
    zip_ref = zipfile.ZipFile(filepath, 'r')
    zip_ref.extractall(dest_directory)
    zip_ref.close()