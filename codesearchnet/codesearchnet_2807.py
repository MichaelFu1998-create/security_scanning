def get_heron_options_from_env():
    """Retrieves heron options from the `HERON_OPTIONS` environment variable.

    Heron options have the following format:

        cmdline.topologydefn.tmpdirectory=/var/folders/tmpdir
        cmdline.topology.initial.state=PAUSED

    In this case, the returned map will contain:

        #!json
        {
          "cmdline.topologydefn.tmpdirectory": "/var/folders/tmpdir",
          "cmdline.topology.initial.state": "PAUSED"
        }

    Currently supports the following options natively:

    - `cmdline.topologydefn.tmpdirectory`: (required) the directory to which this
    topology's defn file is written
    - `cmdline.topology.initial.state`: (default: "RUNNING") the initial state of the topology
    - `cmdline.topology.name`: (default: class name) topology name on deployment

    Returns: map mapping from key to value
    """
    heron_options_raw = os.environ.get("HERON_OPTIONS")
    if heron_options_raw is None:
      raise RuntimeError("HERON_OPTIONS environment variable not found")

    options = {}
    for option_line in heron_options_raw.replace("%%%%", " ").split(','):
      key, sep, value = option_line.partition("=")
      if sep:
        options[key] = value
      else:
        raise ValueError("Invalid HERON_OPTIONS part %r" % option_line)
    return options