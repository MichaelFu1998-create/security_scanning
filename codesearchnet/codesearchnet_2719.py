def template_scheduler_yaml(cl_args, masters):
  '''
  Template scheduler.yaml
  '''
  single_master = masters[0]
  scheduler_config_actual = "%s/standalone/scheduler.yaml" % cl_args["config_path"]

  scheduler_config_template = "%s/standalone/templates/scheduler.template.yaml" \
                              % cl_args["config_path"]
  template_file(scheduler_config_template, scheduler_config_actual,
                {"<scheduler_uri>": "http://%s:4646" % single_master})