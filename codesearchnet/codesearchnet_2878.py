def get_heron_config():
  '''
  Get config opts from the global variable
  :return:
  '''
  opt_list = []
  for (key, value) in config_opts.items():
    opt_list.append('%s=%s' % (key, value))

  all_opts = (','.join(opt_list)).replace(' ', '%%%%')
  return all_opts