def _regex_replacement(self, target, replacement):
      """Regex substitute target with replacement"""
      match = re.compile(target)
      self.data = match.sub(replacement, self.data)