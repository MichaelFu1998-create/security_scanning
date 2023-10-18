def _extract_input_processes(self):
    """
    Given user input of interested processes, it will extract the info and output a list of tuples.
    - input can be multiple values, separated by space;
    - either pid or process_name is optional
    - e.g., "10001/python 10002/java cpp"
    :return: None
    """
    for proc in self.processes:
      ends = proc.split('/')
      pid, name = self._get_tuple(ends)
      self.input_processes.append((pid, name))