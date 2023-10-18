def decode(rawstr, json_loads=default_json_loads):
    """
    Decode a rawstr packet arriving from the socket into a dict.
    """
    decoded_msg = {}
    try:
        # Handle decoding in Python<3.
        rawstr = rawstr.decode('utf-8')
    except AttributeError:
        pass
    split_data = rawstr.split(":", 3)
    msg_type = split_data[0]
    msg_id = split_data[1]
    endpoint = split_data[2]

    data = ''

    if msg_id != '':
        if "+" in msg_id:
            msg_id = msg_id.split('+')[0]
            decoded_msg['id'] = int(msg_id)
            decoded_msg['ack'] = 'data'
        else:
            decoded_msg['id'] = int(msg_id)
            decoded_msg['ack'] = True

    # common to every message
    msg_type_id = int(msg_type)
    if msg_type_id in MSG_VALUES:
        decoded_msg['type'] = MSG_VALUES[int(msg_type)]
    else:
        raise Exception("Unknown message type: %s" % msg_type)

    decoded_msg['endpoint'] = endpoint

    if len(split_data) > 3:
        data = split_data[3]

    if msg_type == "0":  # disconnect
        pass

    elif msg_type == "1":  # connect
        decoded_msg['qs'] = data

    elif msg_type == "2":  # heartbeat
        pass

    elif msg_type == "3":  # message
        decoded_msg['data'] = data

    elif msg_type == "4":  # json msg
        decoded_msg['data'] = json_loads(data)

    elif msg_type == "5":  # event
        try:
            data = json_loads(data)
        except ValueError:
            print("Invalid JSON event message", data)
            decoded_msg['args'] = []
        else:
            decoded_msg['name'] = data.pop('name')
            if 'args' in data:
                decoded_msg['args'] = data['args']
            else:
                decoded_msg['args'] = []

    elif msg_type == "6":  # ack
        if '+' in data:
            ackId, data = data.split('+')
            decoded_msg['ackId'] = int(ackId)
            decoded_msg['args'] = json_loads(data)
        else:
            decoded_msg['ackId'] = int(data)
            decoded_msg['args'] = []

    elif msg_type == "7":  # error
        if '+' in data:
            reason, advice = data.split('+')
            decoded_msg['reason'] = REASONS_VALUES[int(reason)]
            decoded_msg['advice'] = ADVICES_VALUES[int(advice)]
        else:
            decoded_msg['advice'] = ''
            if data != '':
                decoded_msg['reason'] = REASONS_VALUES[int(data)]
            else:
                decoded_msg['reason'] = ''

    elif msg_type == "8":  # noop
        pass

    return decoded_msg