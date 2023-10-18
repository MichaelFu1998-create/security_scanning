def _flatten_listener(listener):
    """
    from

    {
      "Listener": {
        "InstancePort": 80,
        "LoadBalancerPort": 80,
        "Protocol": "HTTP",
        "InstanceProtocol": "HTTP"
      },
      "PolicyNames": []
    },

    to

    {
        "InstancePort": 80,
        "LoadBalancerPort": 80,
        "Protocol": "HTTP",
        "InstanceProtocol": "HTTP",
        "PolicyNames": []
    }
    """
    result = dict()
    if set(listener.keys()) == set(['Listener', 'PolicyNames']):
        result.update(listener['Listener'])
        result['PolicyNames'] = listener['PolicyNames']
    else:
        result = dict(listener)
    return result