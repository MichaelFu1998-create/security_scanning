def run_server(command, cl_args, action, extra_args=dict()):
  '''
  helper function to take action on topologies using REST API
  :param command:
  :param cl_args:
  :param action:        description of action taken
  :return:
  '''
  topology_name = cl_args['topology-name']

  service_endpoint = cl_args['service_url']
  apiroute = rest.ROUTE_SIGNATURES[command][1] % (
      cl_args['cluster'],
      cl_args['role'],
      cl_args['environ'],
      topology_name
  )
  service_apiurl = service_endpoint + apiroute
  service_method = rest.ROUTE_SIGNATURES[command][0]

  # convert the dictionary to a list of tuples
  data = flatten_args(extra_args)

  err_msg = "Failed to %s: %s" % (action, topology_name)
  succ_msg = "Successfully %s: %s" % (action, topology_name)

  try:
    r = service_method(service_apiurl, data=data)
    s = Status.Ok if r.status_code == requests.codes.ok else Status.HeronError
    if r.status_code != requests.codes.ok:
      Log.error(r.json().get('message', "Unknown error from API server %d" % r.status_code))
  except (requests.exceptions.ConnectionError, requests.exceptions.HTTPError) as err:
    Log.error(err)
    return SimpleResult(Status.HeronError, err_msg, succ_msg)

  return SimpleResult(s, err_msg, succ_msg)