def minify(self, css):
      """Tries to minimize the length of CSS code passed as parameter. Returns string."""
      css = css.replace("\r\n", "\n") # get rid of Windows line endings, if they exist
      for rule in _REPLACERS[self.level]:
          css = re.compile(rule[0], re.MULTILINE|re.UNICODE|re.DOTALL).sub(rule[1], css)
      return css