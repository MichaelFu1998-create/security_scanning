def run(command, parser, cl_args, unknown_args):
  '''
  :param command:
  :param parser:
  :param cl_args:
  :param unknown_args:
  :return:
  '''
  Log.debug("Restart Args: %s", cl_args)
  container_id = cl_args['container-id']

  if cl_args['deploy_mode'] == config.SERVER_MODE:
    dict_extra_args = {"container_id": str(container_id)}
    return cli_helper.run_server(command, cl_args, "restart topology", extra_args=dict_extra_args)
  else:
    list_extra_args = ["--container_id", str(container_id)]
    return cli_helper.run_direct(command, cl_args, "restart topology", extra_args=list_extra_args)