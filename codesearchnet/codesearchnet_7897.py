def encode(data, json_dumps=default_json_dumps):
    """
    Encode an attribute dict into a byte string.
    """
    payload = ''
    msg = str(MSG_TYPES[data['type']])

    if msg in ['0', '1']:
        # '1::' [path] [query]
        msg += '::' + data['endpoint']
        if 'qs' in data and data['qs'] != '':
            msg += ':' + data['qs']

    elif msg == '2':
        # heartbeat
        msg += '::'

    elif msg in ['3', '4', '5']:
        # '3:' [id ('+')] ':' [endpoint] ':' [data]
        # '4:' [id ('+')] ':' [endpoint] ':' [json]
        # '5:' [id ('+')] ':' [endpoint] ':' [json encoded event]
        # The message id is an incremental integer, required for ACKs.
        # If the message id is followed by a +, the ACK is not handled by
        # socket.io, but by the user instead.
        if msg == '3':
            payload = data['data']
        if msg == '4':
            payload = json_dumps(data['data'])
        if msg == '5':
            d = {}
            d['name'] = data['name']
            if 'args' in data and data['args'] != []:
                d['args'] = data['args']
            payload = json_dumps(d)
        if 'id' in data:
            msg += ':' + str(data['id'])
            if data['ack'] == 'data':
                msg += '+'
            msg += ':'
        else:
            msg += '::'
        if 'endpoint' not in data:
            data['endpoint'] = ''
        if payload != '':
            msg += data['endpoint'] + ':' + payload
        else:
            msg += data['endpoint']

    elif msg == '6':
        # '6:::' [id] '+' [data]
        msg += '::' + data.get('endpoint', '') + ':' + str(data['ackId'])
        if 'args' in data and data['args'] != []:
            msg += '+' + json_dumps(data['args'])

    elif msg == '7':
        # '7::' [endpoint] ':' [reason] '+' [advice]
        msg += ':::'
        if 'reason' in data and data['reason'] != '':
            msg += str(ERROR_REASONS[data['reason']])
        if 'advice' in data and data['advice'] != '':
            msg += '+' + str(ERROR_ADVICES[data['advice']])
        msg += data['endpoint']

    # NoOp, used to close a poll after the polling duration time
    elif msg == '8':
        msg += '::'

    return msg