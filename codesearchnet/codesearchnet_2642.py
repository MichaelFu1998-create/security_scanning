def get(self, path):
    """ get method """
    t = Template(utils.get_asset("file.html"))
    if path is None:
      self.set_status(404)
      self.write("No such file")
      self.finish()
      return

    if not utils.check_path(path):
      self.write("Only relative paths are allowed")
      self.set_status(403)
      self.finish()
      return

    args = dict(
        filename=path,
        jquery=utils.get_asset("jquery.js"),
        pailer=utils.get_asset("jquery.pailer.js"),
        css=utils.get_asset("bootstrap.css"),
    )
    self.write(t.generate(**args))
    self.finish()