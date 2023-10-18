def convert_to_G(self, word):
    """
    Given a size such as '2333M', return the converted value in G
    """
    value = 0.0
    if word[-1] == 'G' or word[-1] == 'g':
      value = float(word[:-1])
    elif word[-1] == 'M' or word[-1] == 'm':
      value = float(word[:-1]) / 1000.0
    elif word[-1] == 'K' or word[-1] == 'k':
      value = float(word[:-1]) / 1000.0 / 1000.0
    else:  # No unit
      value = float(word) / 1000.0 / 1000.0 / 1000.0
    return str(value)