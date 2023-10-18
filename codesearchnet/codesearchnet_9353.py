def _validate_paths_or_fail(uri, recursive):
    """Do basic validation of the uri, return the path and filename."""
    path, filename = os.path.split(uri)

    # dsub could support character ranges ([0-9]) with some more work, but for
    # now we assume that basic asterisk wildcards are sufficient. Reject any URI
    # that includes square brackets or question marks, since we know that
    # if they actually worked, it would be accidental.
    if '[' in uri or ']' in uri:
      raise ValueError(
          'Square bracket (character ranges) are not supported: %s' % uri)
    if '?' in uri:
      raise ValueError('Question mark wildcards are not supported: %s' % uri)

    # Only support file URIs and *filename* wildcards
    # Wildcards at the directory level or "**" syntax would require better
    # support from the Pipelines API *or* doing expansion here and
    # (potentially) producing a series of FileParams, instead of one.
    if '*' in path:
      raise ValueError(
          'Path wildcard (*) are only supported for files: %s' % uri)
    if '**' in filename:
      raise ValueError('Recursive wildcards ("**") not supported: %s' % uri)
    if filename in ('..', '.'):
      raise ValueError('Path characters ".." and "." not supported '
                       'for file names: %s' % uri)

    # Do not allow non-recursive IO to reference directories.
    if not recursive and not filename:
      raise ValueError('Input or output values that are not recursive must '
                       'reference a filename or wildcard: %s' % uri)