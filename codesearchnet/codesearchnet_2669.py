def parse_args(args):
    """Uses python argparse to collect positional args"""
    Log.info("Input args: %r" % args)

    parser = argparse.ArgumentParser()

    parser.add_argument("--shard", type=int, required=True)
    parser.add_argument("--topology-name", required=True)
    parser.add_argument("--topology-id", required=True)
    parser.add_argument("--topology-defn-file", required=True)
    parser.add_argument("--state-manager-connection", required=True)
    parser.add_argument("--state-manager-root", required=True)
    parser.add_argument("--state-manager-config-file", required=True)
    parser.add_argument("--tmaster-binary", required=True)
    parser.add_argument("--stmgr-binary", required=True)
    parser.add_argument("--metrics-manager-classpath", required=True)
    parser.add_argument("--instance-jvm-opts", required=True)
    parser.add_argument("--classpath", required=True)
    parser.add_argument("--master-port", required=True)
    parser.add_argument("--tmaster-controller-port", required=True)
    parser.add_argument("--tmaster-stats-port", required=True)
    parser.add_argument("--heron-internals-config-file", required=True)
    parser.add_argument("--override-config-file", required=True)
    parser.add_argument("--component-ram-map", required=True)
    parser.add_argument("--component-jvm-opts", required=True)
    parser.add_argument("--pkg-type", required=True)
    parser.add_argument("--topology-binary-file", required=True)
    parser.add_argument("--heron-java-home", required=True)
    parser.add_argument("--shell-port", required=True)
    parser.add_argument("--heron-shell-binary", required=True)
    parser.add_argument("--metrics-manager-port", required=True)
    parser.add_argument("--cluster", required=True)
    parser.add_argument("--role", required=True)
    parser.add_argument("--environment", required=True)
    parser.add_argument("--instance-classpath", required=True)
    parser.add_argument("--metrics-sinks-config-file", required=True)
    parser.add_argument("--scheduler-classpath", required=True)
    parser.add_argument("--scheduler-port", required=True)
    parser.add_argument("--python-instance-binary", required=True)
    parser.add_argument("--cpp-instance-binary", required=True)
    parser.add_argument("--metricscache-manager-classpath", required=True)
    parser.add_argument("--metricscache-manager-master-port", required=True)
    parser.add_argument("--metricscache-manager-stats-port", required=True)
    parser.add_argument("--metricscache-manager-mode", required=False)
    parser.add_argument("--is-stateful", required=True)
    parser.add_argument("--checkpoint-manager-classpath", required=True)
    parser.add_argument("--checkpoint-manager-port", required=True)
    parser.add_argument("--checkpoint-manager-ram", type=long, required=True)
    parser.add_argument("--stateful-config-file", required=True)
    parser.add_argument("--health-manager-mode", required=True)
    parser.add_argument("--health-manager-classpath", required=True)
    parser.add_argument("--jvm-remote-debugger-ports", required=False,
                        help="ports to be used by a remote debugger for JVM instances")

    parsed_args, unknown_args = parser.parse_known_args(args[1:])

    if unknown_args:
      Log.error('Unknown argument: %s' % unknown_args[0])
      parser.print_help()
      sys.exit(1)

    return parsed_args