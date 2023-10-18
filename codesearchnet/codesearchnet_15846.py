def find_header(self, infile):
    """
    Parses the file and tries to find the header line. The header line has format:

      2014-10-29 00:28:42.15161        CPU0   CPU1   CPU2   CPU3  ...

    So should always have CPU# for each core. This function verifies a good header and
    returns the list of CPUs that exist from the header.

    :param infile: The opened file in read mode to find the header.
    :return cpus: A list of the core names so in this example ['CPU0', 'CPU1', ...]
    """
    cpus = []
    for line in infile:  # Pre-processing - Try to find header
      if not self.is_header_line(line):
        continue
      # Verifying correctness of the header
      cpu_header = line.split()
      for cpu_h in cpu_header[2:]:
        if not cpu_h.startswith('CPU'):
          cpus = []  # Bad header so reset to nothing
          break
        else:
          cpus.append(cpu_h)
      if len(cpus) > 0:  # We found the header
        break
    return cpus