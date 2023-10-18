def template_statemgr_yaml(cl_args, zookeepers):
  '''
  Template statemgr.yaml
  '''
  statemgr_config_file_template = "%s/standalone/templates/statemgr.template.yaml" \
                                  % cl_args["config_path"]
  statemgr_config_file_actual = "%s/standalone/statemgr.yaml" % cl_args["config_path"]

  template_file(statemgr_config_file_template, statemgr_config_file_actual,
                {"<zookeeper_host:zookeeper_port>": ",".join(
                    ['"%s"' % zk if ":" in zk else '"%s:2181"' % zk for zk in zookeepers])})