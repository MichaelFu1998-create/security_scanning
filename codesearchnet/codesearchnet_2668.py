def init_from_parsed_args(self, parsed_args):
    """ initialize from parsed arguments """
    self.shard = parsed_args.shard
    self.topology_name = parsed_args.topology_name
    self.topology_id = parsed_args.topology_id
    self.topology_defn_file = parsed_args.topology_defn_file
    self.state_manager_connection = parsed_args.state_manager_connection
    self.state_manager_root = parsed_args.state_manager_root
    self.state_manager_config_file = parsed_args.state_manager_config_file
    self.tmaster_binary = parsed_args.tmaster_binary
    self.stmgr_binary = parsed_args.stmgr_binary
    self.metrics_manager_classpath = parsed_args.metrics_manager_classpath
    self.metricscache_manager_classpath = parsed_args.metricscache_manager_classpath
    # '=' can be parsed in a wrong way by some schedulers (aurora) hence it needs to be escaped.
    # It is escaped in two different ways. '(61)' is the new escaping. '&equals;' was
    # the original replacement but it is not friendly to bash and is causing issues. The original
    # escaping is still left there for reference and backward compatibility purposes (to be
    # removed after no topology needs it)
    self.instance_jvm_opts =\
        base64.b64decode(parsed_args.instance_jvm_opts.lstrip('"').
                         rstrip('"').replace('(61)', '=').replace('&equals;', '='))
    self.classpath = parsed_args.classpath
    # Needed for Docker environments since the hostname of a docker container is the container's
    # id within docker, rather than the host's hostname. NOTE: this 'HOST' env variable is not
    # guaranteed to be set in all Docker executor environments (outside of Marathon)
    if is_docker_environment():
      self.master_host = os.environ.get('HOST') if 'HOST' in os.environ else socket.gethostname()
    else:
      self.master_host = socket.gethostname()
    self.master_port = parsed_args.master_port
    self.tmaster_controller_port = parsed_args.tmaster_controller_port
    self.tmaster_stats_port = parsed_args.tmaster_stats_port
    self.heron_internals_config_file = parsed_args.heron_internals_config_file
    self.override_config_file = parsed_args.override_config_file
    self.component_ram_map =\
        map(lambda x: {x.split(':')[0]:
                           int(x.split(':')[1])}, parsed_args.component_ram_map.split(','))
    self.component_ram_map =\
        functools.reduce(lambda x, y: dict(x.items() + y.items()), self.component_ram_map)

    # component_jvm_opts_in_base64 itself is a base64-encoding-json-map, which is appended with
    # " at the start and end. It also escapes "=" to "&equals" due to aurora limitation
    # And the json is a map from base64-encoding-component-name to base64-encoding-jvm-options
    self.component_jvm_opts = {}
    # First we need to decode the base64 string back to a json map string.
    # '=' can be parsed in a wrong way by some schedulers (aurora) hence it needs to be escaped.
    # It is escaped in two different ways. '(61)' is the new escaping. '&equals;' was
    # the original replacement but it is not friendly to bash and is causing issues. The original
    # escaping is still left there for reference and backward compatibility purposes (to be
    # removed after no topology needs it)
    component_jvm_opts_in_json =\
        base64.b64decode(parsed_args.component_jvm_opts.
                         lstrip('"').rstrip('"').replace('(61)', '=').replace('&equals;', '='))
    if component_jvm_opts_in_json != "":
      for (k, v) in json.loads(component_jvm_opts_in_json).items():
        # In json, the component name and JVM options are still in base64 encoding
        self.component_jvm_opts[base64.b64decode(k)] = base64.b64decode(v)

    self.pkg_type = parsed_args.pkg_type
    self.topology_binary_file = parsed_args.topology_binary_file
    self.heron_java_home = parsed_args.heron_java_home
    self.shell_port = parsed_args.shell_port
    self.heron_shell_binary = parsed_args.heron_shell_binary
    self.metrics_manager_port = parsed_args.metrics_manager_port
    self.metricscache_manager_master_port = parsed_args.metricscache_manager_master_port
    self.metricscache_manager_stats_port = parsed_args.metricscache_manager_stats_port
    self.cluster = parsed_args.cluster
    self.role = parsed_args.role
    self.environment = parsed_args.environment
    self.instance_classpath = parsed_args.instance_classpath
    self.metrics_sinks_config_file = parsed_args.metrics_sinks_config_file
    self.scheduler_classpath = parsed_args.scheduler_classpath
    self.scheduler_port = parsed_args.scheduler_port
    self.python_instance_binary = parsed_args.python_instance_binary
    self.cpp_instance_binary = parsed_args.cpp_instance_binary

    self.is_stateful_topology = (parsed_args.is_stateful.lower() == 'true')
    self.checkpoint_manager_classpath = parsed_args.checkpoint_manager_classpath
    self.checkpoint_manager_port = parsed_args.checkpoint_manager_port
    self.checkpoint_manager_ram = parsed_args.checkpoint_manager_ram
    self.stateful_config_file = parsed_args.stateful_config_file
    self.metricscache_manager_mode = parsed_args.metricscache_manager_mode \
        if parsed_args.metricscache_manager_mode else "disabled"
    self.health_manager_mode = parsed_args.health_manager_mode
    self.health_manager_classpath = '%s:%s'\
        % (self.scheduler_classpath, parsed_args.health_manager_classpath)
    self.jvm_remote_debugger_ports = \
      parsed_args.jvm_remote_debugger_ports.split(",") \
        if parsed_args.jvm_remote_debugger_ports else None