def CheckEnd(self, filename, clean_lines, linenum, error):
    """Check end of namespace comments."""
    line = clean_lines.raw_lines[linenum]

    # Check how many lines is enclosed in this namespace.  Don't issue
    # warning for missing namespace comments if there aren't enough
    # lines.  However, do apply checks if there is already an end of
    # namespace comment and it's incorrect.
    #
    # TODO(unknown): We always want to check end of namespace comments
    # if a namespace is large, but sometimes we also want to apply the
    # check if a short namespace contained nontrivial things (something
    # other than forward declarations).  There is currently no logic on
    # deciding what these nontrivial things are, so this check is
    # triggered by namespace size only, which works most of the time.
    if (linenum - self.starting_linenum < 10
        and not Match(r'^\s*};*\s*(//|/\*).*\bnamespace\b', line)):
      return

    # Look for matching comment at end of namespace.
    #
    # Note that we accept C style "/* */" comments for terminating
    # namespaces, so that code that terminate namespaces inside
    # preprocessor macros can be cpplint clean.
    #
    # We also accept stuff like "// end of namespace <name>." with the
    # period at the end.
    #
    # Besides these, we don't accept anything else, otherwise we might
    # get false negatives when existing comment is a substring of the
    # expected namespace.
    if self.name:
      # Named namespace
      if not Match((r'^\s*};*\s*(//|/\*).*\bnamespace\s+' +
                    re.escape(self.name) + r'[\*/\.\\\s]*$'),
                   line):
        error(filename, linenum, 'readability/namespace', 5,
              'Namespace should be terminated with "// namespace %s"' %
              self.name)
    else:
      # Anonymous namespace
      if not Match(r'^\s*};*\s*(//|/\*).*\bnamespace[\*/\.\\\s]*$', line):
        # If "// namespace anonymous" or "// anonymous namespace (more text)",
        # mention "// anonymous namespace" as an acceptable form
        if Match(r'^\s*}.*\b(namespace anonymous|anonymous namespace)\b', line):
          error(filename, linenum, 'readability/namespace', 5,
                'Anonymous namespace should be terminated with "// namespace"'
                ' or "// anonymous namespace"')
        else:
          error(filename, linenum, 'readability/namespace', 5,
                'Anonymous namespace should be terminated with "// namespace"')