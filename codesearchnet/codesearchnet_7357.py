def consume(consumer_id):
    """Given an existing consumer ID, return any new lines from the
    log since the last time the consumer was consumed."""
    global _consumers
    consumer = _consumers[consumer_id]

    client = get_docker_client()
    try:
        status = client.inspect_container(consumer.container_id)['State']['Status']
    except Exception as e:
        status = 'unknown'
    new_logs = client.logs(consumer.container_id,
                           stdout=True,
                           stderr=True,
                           stream=False,
                           timestamps=False,
                           since=calendar.timegm(consumer.offset.timetuple()))

    updated_consumer = Consumer(consumer.container_id, datetime.utcnow())
    _consumers[str(consumer_id)] = updated_consumer

    response = jsonify({'logs': new_logs, 'status': status})
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST'
    return response