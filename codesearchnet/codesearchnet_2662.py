def get(self, path):
    """ get method """

    logging.debug("request to download: %s", path)
    # If the file is large, we want to abandon downloading
    # if user cancels the requests.
    # pylint: disable=attribute-defined-outside-init
    self.connection_closed = False

    self.set_header("Content-Disposition", "attachment")
    if not utils.check_path(path):
      self.write("Only relative paths are allowed")
      self.set_status(403)
      self.finish()
      return

    if path is None or not os.path.isfile(path):
      self.write("File %s  not found" % path)
      self.set_status(404)
      self.finish()
      return

    length = int(4 * 1024 * 1024)
    offset = int(0)
    while True:
      data = utils.read_chunk(path, offset=offset, length=length, escape_data=False)
      if self.connection_closed or 'data' not in data or len(data['data']) < length:
        break
      offset += length
      self.write(data['data'])
      self.flush()

    if 'data' in data:
      self.write(data['data'])
    self.finish()