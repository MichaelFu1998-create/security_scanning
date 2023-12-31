def format():
    """
        Formats the output of another tool in the given way.
        Has default styles for ranges, hosts and services.
    """
    argparser = argparse.ArgumentParser(description='Formats a json object in a certain way. Use with pipes.')
    argparser.add_argument('format', metavar='format', help='How to format the json for example "{address}:{port}".', nargs='?')
    arguments = argparser.parse_args()
    service_style = "{address:15} {port:7} {protocol:5} {service:15} {state:10} {banner} {tags}"
    host_style = "{address:15} {tags}"
    ranges_style = "{range:18} {tags}"
    users_style = "{username}"
    if arguments.format:
        format_input(arguments.format)
    else:
        doc_mapper = DocMapper()
        if doc_mapper.is_pipe:
            for obj in doc_mapper.get_pipe():
                style = ''
                if isinstance(obj, Range):
                    style = ranges_style
                elif isinstance(obj, Host):
                    style = host_style
                elif isinstance(obj, Service):
                    style = service_style
                elif isinstance(obj, User):
                    style = users_style
                print_line(fmt.format(style, **obj.to_dict(include_meta=True)))
        else:
            print_error("Please use this script with pipes")