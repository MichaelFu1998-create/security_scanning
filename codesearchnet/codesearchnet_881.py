def normalizeStreamSources(self):
    """
    TODO: document
    """
    task = dict(self.__control)
    if 'dataset' in task:
      for stream in task['dataset']['streams']:
        self.normalizeStreamSource(stream)
    else:
      for subtask in task['tasks']:
        for stream in subtask['dataset']['streams']:
          self.normalizeStreamSource(stream)