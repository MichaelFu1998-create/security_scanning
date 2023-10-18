def run(command, parser, cl_args, unknown_args):
  '''
  runs parser
  '''
  action = cl_args["action"]
  if action == Action.SET:
    call_editor(get_inventory_file(cl_args))
    update_config_files(cl_args)
  elif action == Action.CLUSTER:
    action_type = cl_args["type"]
    if action_type == Cluster.START:
      start_cluster(cl_args)
    elif action_type == Cluster.STOP:
      if check_sure(cl_args, "Are you sure you want to stop the cluster?"
                             " This will terminate everything running in "
                             "the cluster and remove any scheduler state."):

        stop_cluster(cl_args)
    else:
      raise ValueError("Invalid cluster action %s" % action_type)
  elif action == Action.TEMPLATE:
    update_config_files(cl_args)
  elif action == Action.GET:
    action_type = cl_args["type"]
    if action_type == Get.SERVICE_URL:
      print get_service_url(cl_args)
    elif action_type == Get.HERON_UI_URL:
      print get_heron_ui_url(cl_args)
    elif action_type == Get.HERON_TRACKER_URL:
      print get_heron_tracker_url(cl_args)
    else:
      raise ValueError("Invalid get action %s" % action_type)
  elif action == Action.INFO:
    print_cluster_info(cl_args)
  else:
    raise ValueError("Invalid action %s" % action)

  return SimpleResult(Status.Ok)