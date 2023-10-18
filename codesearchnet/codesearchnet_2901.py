def get(self, path):
    ''' get method '''
    if not path:
      path = "."

    if not utils.check_path(path):
      self.write("Only relative paths are allowed")
      self.set_status(403)
      self.finish()
      return

    t = Template(utils.get_asset("browse.html"))
    args = dict(
        path=path,
        listing=utils.get_listing(path),
        format_prefix=utils.format_prefix,
        stat=stat,
        get_stat=utils.get_stat,
        os=os,
        css=utils.get_asset("bootstrap.css")
    )
    self.write(t.generate(**args))
    self.finish()