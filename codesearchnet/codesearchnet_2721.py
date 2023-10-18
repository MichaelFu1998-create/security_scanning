def template_apiserver_hcl(cl_args, masters, zookeepers):
  """
  template apiserver.hcl
  """
  single_master = masters[0]
  apiserver_config_template = "%s/standalone/templates/apiserver.template.hcl" \
                              % cl_args["config_path"]
  apiserver_config_actual = "%s/standalone/resources/apiserver.hcl" % cl_args["config_path"]

  replacements = {
      "<heron_apiserver_hostname>": '"%s"' % get_hostname(single_master, cl_args),
      "<heron_apiserver_executable>": '"%s/heron-apiserver"'
                                      % config.get_heron_bin_dir()
                                      if is_self(single_master)
                                      else '"%s/.heron/bin/heron-apiserver"'
                                      % get_remote_home(single_master, cl_args),
      "<zookeeper_host:zookeeper_port>": ",".join(
          ['%s' % zk if ":" in zk else '%s:2181' % zk for zk in zookeepers]),
      "<scheduler_uri>": "http://%s:4646" % single_master
  }

  template_file(apiserver_config_template, apiserver_config_actual, replacements)