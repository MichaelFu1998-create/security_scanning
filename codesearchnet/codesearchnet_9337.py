def _name_for_command(command):
  r"""Craft a simple command name from the command.

  The best command strings for this are going to be those where a simple
  command was given; we will use the command to derive the name.

  We won't always be able to figure something out and the caller should just
  specify a "--name" on the command-line.

  For example, commands like "export VAR=val\necho ${VAR}", this function would
  return "export".

  If the command starts space or a comment, then we'll skip to the first code
  we can find.

  If we find nothing, just return "command".

  >>> _name_for_command('samtools index "${BAM}"')
  'samtools'
  >>> _name_for_command('/usr/bin/sort "${INFILE}" > "${OUTFILE}"')
  'sort'
  >>> _name_for_command('# This should be ignored')
  'command'
  >>> _name_for_command('\\\n\\\n# Bad continuations, but ignore.\necho hello.')
  'echo'

  Arguments:
    command: the user-provided command
  Returns:
    a proposed name for the task.
  """

  lines = command.splitlines()
  for line in lines:
    line = line.strip()
    if line and not line.startswith('#') and line != '\\':
      return os.path.basename(re.split(r'\s', line)[0])

  return 'command'