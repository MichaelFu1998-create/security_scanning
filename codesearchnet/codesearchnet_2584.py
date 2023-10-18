def get(self, path):
    """ get method """
    if path is None:
      return {}

    if not utils.check_path(path):
      self.write("Only relative paths are allowed")
      self.set_status(403)
      self.finish()
      return

    offset = self.get_argument("offset", default=-1)
    length = self.get_argument("length", default=-1)
    if not os.path.isfile(path):
      return {}
    data = utils.read_chunk(path, offset=offset, length=length, escape_data=True)
    self.write(json.dumps(data))
    self.finish()