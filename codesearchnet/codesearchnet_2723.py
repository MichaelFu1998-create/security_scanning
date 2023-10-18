def template_heron_tools_hcl(cl_args, masters, zookeepers):
  '''
  template heron tools
  '''
  heron_tools_hcl_template = "%s/standalone/templates/heron_tools.template.hcl" \
                             % cl_args["config_path"]
  heron_tools_hcl_actual = "%s/standalone/resources/heron_tools.hcl" \
                             % cl_args["config_path"]

  single_master = masters[0]
  template_file(heron_tools_hcl_template, heron_tools_hcl_actual,
                {
                    "<zookeeper_host:zookeeper_port>": ",".join(
                        ['%s' % zk if ":" in zk else '%s:2181' % zk for zk in zookeepers]),
                    "<heron_tracker_executable>": '"%s/heron-tracker"' % config.get_heron_bin_dir(),
                    "<heron_tools_hostname>": '"%s"' % get_hostname(single_master, cl_args),
                    "<heron_ui_executable>": '"%s/heron-ui"' % config.get_heron_bin_dir()
                })