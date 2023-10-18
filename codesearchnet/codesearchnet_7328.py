def _nginx_location_spec(port_spec, bridge_ip):
    """This will output the nginx location config string for specific port spec """
    location_string_spec = "\t \t location / { \n"
    for location_setting in ['proxy_http_version 1.1;',
                             'proxy_set_header Upgrade $http_upgrade;',
                             'proxy_set_header Connection "upgrade";',
                             'proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;',
                             'proxy_set_header Host $http_host;',
                             _nginx_proxy_string(port_spec, bridge_ip)]:
        location_string_spec += "\t \t \t {} \n".format(location_setting)
    location_string_spec += "\t \t } \n"
    return location_string_spec