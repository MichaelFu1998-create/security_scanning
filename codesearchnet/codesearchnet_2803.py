def create_socket_options():
  """Creates SocketOptions object from a given sys_config dict"""
  sys_config = system_config.get_sys_config()
  opt_list = [const.INSTANCE_NETWORK_WRITE_BATCH_SIZE_BYTES,
              const.INSTANCE_NETWORK_WRITE_BATCH_TIME_MS,
              const.INSTANCE_NETWORK_READ_BATCH_SIZE_BYTES,
              const.INSTANCE_NETWORK_READ_BATCH_TIME_MS,
              const.INSTANCE_NETWORK_OPTIONS_SOCKET_RECEIVED_BUFFER_SIZE_BYTES,
              const.INSTANCE_NETWORK_OPTIONS_SOCKET_SEND_BUFFER_SIZE_BYTES]

  Log.debug("In create_socket_options()")
  try:
    value_lst = [int(sys_config[opt]) for opt in opt_list]
    sock_opt = SocketOptions(*value_lst)
    return sock_opt
  except ValueError as e:
    # couldn't convert to int
    raise ValueError("Invalid value in sys_config: %s" % str(e))
  except KeyError as e:
    # option key was not found
    raise KeyError("Incomplete sys_config: %s" % str(e))