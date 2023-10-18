def heron_class(class_name, lib_jars, extra_jars=None, args=None, java_defines=None):
  '''
  Execute a heron class given the args and the jars needed for class path
  :param class_name:
  :param lib_jars:
  :param extra_jars:
  :param args:
  :param java_defines:
  :return:
  '''
  # default optional params to empty list if not provided
  if extra_jars is None:
    extra_jars = []
  if args is None:
    args = []
  if java_defines is None:
    java_defines = []

  # Format all java -D options that need to be passed while running
  # the class locally.
  java_opts = ['-D' + opt for opt in java_defines]

  # Construct the command line for the sub process to run
  # Because of the way Python execute works,
  # the java opts must be passed as part of the list
  all_args = [config.get_java_path(), "-client", "-Xmx1g"] + \
             java_opts + \
             ["-cp", config.get_classpath(extra_jars + lib_jars)]

  all_args += [class_name] + list(args)

  # set heron_config environment variable
  heron_env = os.environ.copy()
  heron_env['HERON_OPTIONS'] = opts.get_heron_config()

  # print the verbose message
  Log.debug("Invoking class using command: ``%s''", ' '.join(all_args))
  Log.debug("Heron options: {%s}", str(heron_env["HERON_OPTIONS"]))

  # invoke the command with subprocess and print error message, if any
  process = subprocess.Popen(all_args, env=heron_env, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, bufsize=1)
  # stdout message has the information Java program sends back
  # stderr message has extra information, such as debugging message
  return ProcessResult(process)