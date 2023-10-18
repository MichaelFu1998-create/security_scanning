def run(command, parser, cl_args, unknown_args):
  '''
  :param command:
  :param parser:
  :param args:
  :param unknown_args:
  :return:
  '''
  cluster = cl_args['cluster']

  # server mode
  if cluster:
    config_file = config.heron_rc_file()
    client_confs = dict()

    # Read the cluster definition, if not found
    client_confs = cdefs.read_server_mode_cluster_definition(cluster, cl_args, config_file)

    if not client_confs[cluster]:
      Log.error('Neither service url nor %s cluster definition in %s file', cluster, config_file)
      return SimpleResult(Status.HeronError)

    # if cluster definition exists, but service_url is not set, it is an error
    if not 'service_url' in client_confs[cluster]:
      Log.error('No service url for %s cluster in %s', cluster, config_file)
      sys.exit(1)

    service_endpoint = cl_args['service_url']
    service_apiurl = service_endpoint + rest.ROUTE_SIGNATURES[command][1]
    service_method = rest.ROUTE_SIGNATURES[command][0]

    try:
      r = service_method(service_apiurl)
      if r.status_code != requests.codes.ok:
        Log.error(r.json().get('message', "Unknown error from API server %d" % r.status_code))
      sorted_items = sorted(r.json().items(), key=lambda tup: tup[0])
      for key, value in sorted_items:
        print("%s : %s" % (key, value))
    except (requests.exceptions.ConnectionError, requests.exceptions.HTTPError) as err:
      Log.error(err)
      return SimpleResult(Status.HeronError)
  else:
    config.print_build_info()

  return SimpleResult(Status.Ok)