def launch_topology_server(cl_args, topology_file, topology_defn_file, topology_name):
  '''
  Launch a topology given topology jar, its definition file and configurations
  :param cl_args:
  :param topology_file:
  :param topology_defn_file:
  :param topology_name:
  :return:
  '''
  service_apiurl = cl_args['service_url'] + rest.ROUTE_SIGNATURES['submit'][1]
  service_method = rest.ROUTE_SIGNATURES['submit'][0]
  data = dict(
      name=topology_name,
      cluster=cl_args['cluster'],
      role=cl_args['role'],
      environment=cl_args['environ'],
      user=cl_args['submit_user'],
  )

  Log.info("" + str(cl_args))
  overrides = dict()
  if 'config_property' in cl_args:
    overrides = config.parse_override_config(cl_args['config_property'])

  if overrides:
    data.update(overrides)

  if cl_args['dry_run']:
    data["dry_run"] = True

  files = dict(
      definition=open(topology_defn_file, 'rb'),
      topology=open(topology_file, 'rb'),
  )

  err_ctxt = "Failed to launch topology '%s' %s" % (topology_name, launch_mode_msg(cl_args))
  succ_ctxt = "Successfully launched topology '%s' %s" % (topology_name, launch_mode_msg(cl_args))

  try:
    r = service_method(service_apiurl, data=data, files=files)
    ok = r.status_code is requests.codes.ok
    created = r.status_code is requests.codes.created
    s = Status.Ok if created or ok else Status.HeronError
    if s is Status.HeronError:
      Log.error(r.json().get('message', "Unknown error from API server %d" % r.status_code))
    elif ok:
      # this case happens when we request a dry_run
      print(r.json().get("response"))
  except (requests.exceptions.ConnectionError, requests.exceptions.HTTPError) as err:
    Log.error(err)
    return SimpleResult(Status.HeronError, err_ctxt, succ_ctxt)
  return SimpleResult(s, err_ctxt, succ_ctxt)