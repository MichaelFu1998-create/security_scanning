def _nginx_http_spec(port_spec, bridge_ip):
    """This will output the nginx HTTP config string for specific port spec """
    server_string_spec = "\t server {\n"
    server_string_spec += "\t \t {}\n".format(_nginx_max_file_size_string())
    server_string_spec += "\t \t {}\n".format(_nginx_listen_string(port_spec))
    server_string_spec += "\t \t {}\n".format(_nginx_server_name_string(port_spec))
    server_string_spec += _nginx_location_spec(port_spec, bridge_ip)
    server_string_spec += _custom_502_page()
    server_string_spec += "\t }\n"
    return server_string_spec