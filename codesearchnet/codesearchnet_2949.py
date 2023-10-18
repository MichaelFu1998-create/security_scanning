def CheckForCopyright(filename, lines, error):
  """Logs an error if no Copyright message appears at the top of the file."""

  # We'll say it should occur by line 10. Don't forget there's a
  # dummy line at the front.
  for line in range(1, min(len(lines), 11)):
    if re.search(r'Copyright', lines[line], re.I): break
  else:                       # means no copyright line was found
    error(filename, 0, 'legal/copyright', 5,
          'No copyright message found.  '
          'You should have a line: "Copyright [year] <Copyright Owner>"')