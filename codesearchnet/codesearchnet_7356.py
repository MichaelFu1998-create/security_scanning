def register_consumer():
    """Given a hostname and port attempting to be accessed,
    return a unique consumer ID for accessing logs from
    the referenced container."""
    global _consumers
    hostname, port = request.form['hostname'], request.form['port']

    app_name = _app_name_from_forwarding_info(hostname, port)
    containers = get_dusty_containers([app_name], include_exited=True)
    if not containers:
        raise ValueError('No container exists for app {}'.format(app_name))
    container = containers[0]

    new_id = uuid1()
    new_consumer = Consumer(container['Id'], datetime.utcnow())
    _consumers[str(new_id)] = new_consumer

    response = jsonify({'app_name': app_name, 'consumer_id': new_id})
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST'
    return response