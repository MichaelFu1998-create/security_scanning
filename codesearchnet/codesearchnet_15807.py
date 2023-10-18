def process_swap_line(self, words):
    """
    Process the line starting with "Swap:"
    Example log: Swap:   63.998G total,    0.000k used,   63.998G free,   11.324G cached
    For each value, needs to convert to 'G' (needs to handle cases of K, M)
    """
    words = words[1:]
    length = len(words) / 2  # The number of pairs
    values = {}
    for offset in range(length):
      k = words[2 * offset + 1].strip(',')
      v = self.convert_to_G(words[2 * offset])
      values['swap_' + k] = v
    self.put_values_into_data(values)