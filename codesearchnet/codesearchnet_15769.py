def parse_user_defined_metric_classes(config_obj, metric_classes):
  """
  Parse the user defined metric class information
  :param config_obj: ConfigParser object
  :param metric_classes: list of metric classes to be updated
  :return:
  """
  user_defined_metric_list = config_obj.get('GLOBAL', 'user_defined_metrics').split()
  for udm_string in user_defined_metric_list:
    try:
      metric_name, metric_class_name, metric_file = udm_string.split(':')
    except ValueError:
      logger.error('Bad user defined metric specified')
      continue
    module_name = os.path.splitext(os.path.basename(metric_file))[0]
    try:
      new_module = imp.load_source(module_name, metric_file)
      new_class = getattr(new_module, metric_class_name)
      if metric_name in metric_classes.keys():
        logger.warn('Overriding pre-defined metric class definition for ', metric_name)
      metric_classes[metric_name] = new_class
    except ImportError:
      logger.error('Something wrong with importing a user defined metric class. Skipping metric: ', metric_name)
      continue