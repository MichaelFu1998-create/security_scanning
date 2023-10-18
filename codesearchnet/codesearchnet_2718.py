def template_slave_hcl(cl_args, masters):
  '''
  Template slave config file
  '''
  slave_config_template = "%s/standalone/templates/slave.template.hcl" % cl_args["config_path"]
  slave_config_actual = "%s/standalone/resources/slave.hcl" % cl_args["config_path"]
  masters_in_quotes = ['"%s"' % master for master in masters]
  template_file(slave_config_template, slave_config_actual,
                {"<nomad_masters:master_port>": ", ".join(masters_in_quotes)})