def process_tasks_line(self, words):
    """
    Process the line starting with "Tasks:"
    Example log:   Tasks: 446 total,   1 running, 442 sleeping,   2 stopped,   1 zombie
    """
    words = words[1:]
    length = len(words) / 2  # The number of pairs
    values = {}
    for offset in range(length):
      k = words[2 * offset + 1].strip(',')
      v = words[2 * offset]
      values['tasks_' + k] = v
    self.put_values_into_data(values)