def getpath(self, section, option):
          """Return option as an expanded path."""
          return os.path.expanduser(os.path.expandvars(self.get(section, option)))