def get(self, path):
    ''' get method '''
    path = tornado.escape.url_unescape(path)
    if not path:
      path = "."

    # User should not be able to access anything outside
    # of the dir that heron-shell is running in. This ensures
    # sandboxing. So we don't allow absolute paths and parent
    # accessing.
    if not utils.check_path(path):
      self.write("Only relative paths are allowed")
      self.set_status(403)
      self.finish()
      return

    listing = utils.get_listing(path)
    file_stats = {}
    for fn in listing:
      try:
        is_dir = False
        formatted_stat = utils.format_prefix(fn, utils.get_stat(path, fn))
        if stat.S_ISDIR(utils.get_stat(path, fn).st_mode):
          is_dir = True
        file_stats[fn] = {
            "formatted_stat": formatted_stat,
            "is_dir": is_dir,
            "path": tornado.escape.url_escape(os.path.join(path, fn)),
        }
        if fn == "..":
          path_fragments = path.split("/")
          if not path_fragments:
            file_stats[fn]["path"] = "."
          else:
            file_stats[fn]["path"] = tornado.escape.url_escape("/".join(path_fragments[:-1]))
      except:
        continue
    self.write(json.dumps(file_stats))
    self.finish()