def get_nginx_configuration_spec(port_spec_dict, docker_bridge_ip):
    """This function will take in a port spec as specified by the port_spec compiler and
    will output an nginx web proxy config string. This string can then be written to a file
    and used running nginx """
    nginx_http_config, nginx_stream_config = "", ""
    for port_spec in port_spec_dict['nginx']:
        if port_spec['type'] == 'http':
            nginx_http_config += _nginx_http_spec(port_spec, docker_bridge_ip)
        elif port_spec['type'] == 'stream':
            nginx_stream_config += _nginx_stream_spec(port_spec, docker_bridge_ip)
    return {'http': nginx_http_config, 'stream': nginx_stream_config}