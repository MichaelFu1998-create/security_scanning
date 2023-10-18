def run(command, parser, cl_args, unknown_args):
  """ run the update command """

  Log.debug("Update Args: %s", cl_args)

  # Build jar list
  extra_lib_jars = jars.packing_jars()
  action = "update topology%s" % (' in dry-run mode' if cl_args["dry_run"] else '')

  # Build extra args
  dict_extra_args = {}
  try:
    dict_extra_args = build_extra_args_dict(cl_args)
  except Exception as err:
    return SimpleResult(Status.InvocationError, err.message)

  # Execute
  if cl_args['deploy_mode'] == config.SERVER_MODE:
    return cli_helper.run_server(command, cl_args, action, dict_extra_args)
  else:
    # Convert extra argument to commandline format and then execute
    list_extra_args = convert_args_dict_to_list(dict_extra_args)
    return cli_helper.run_direct(command, cl_args, action, list_extra_args, extra_lib_jars)