def _nginx_stream_spec(port_spec, bridge_ip):
    """This will output the nginx stream config string for specific port spec """
    server_string_spec = "\t server {\n"
    server_string_spec += "\t \t {}\n".format(_nginx_listen_string(port_spec))
    server_string_spec += "\t \t {}\n".format(_nginx_proxy_string(port_spec, bridge_ip))
    server_string_spec += "\t }\n"
    return server_string_spec