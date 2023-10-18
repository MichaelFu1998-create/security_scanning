def _async_stream_process_output(process, stream_fn, handler):
  """ Stream and handle the output of a process
  :param process: the process to stream the output for
  :param stream_fn: the function that applies handler to process
  :param handler: a function that will be called for each log line
  :return: None
  """
  logging_thread = Thread(target=stream_fn, args=(process, handler, ))

  # Setting the logging thread as a daemon thread will allow it to exit with the program
  # rather than blocking the exit waiting for it to be handled manually.
  logging_thread.daemon = True
  logging_thread.start()

  return logging_thread