def process_cpu_line(self, words):
    """
    Process the line starting with "Cpu(s):"
    Example log: Cpu(s):  1.3%us,  0.5%sy,  0.0%ni, 98.2%id,  0.0%wa,  0.0%hi,  0.0%si,  0.0%st
    """

    values = {}
    for word in words[1:]:
      val, key = word.split('%')
      values['cpu_' + key.strip(',')] = val
    self.put_values_into_data(values)