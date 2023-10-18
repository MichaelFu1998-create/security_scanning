def serve(destination, port, config):
    """Run a simple web server."""
    if os.path.exists(destination):
        pass
    elif os.path.exists(config):
        settings = read_settings(config)
        destination = settings.get('destination')
        if not os.path.exists(destination):
            sys.stderr.write("The '{}' directory doesn't exist, maybe try "
                             "building first?\n".format(destination))
            sys.exit(1)
    else:
        sys.stderr.write("The {destination} directory doesn't exist "
                         "and the config file ({config}) could not be read.\n"
                         .format(destination=destination, config=config))
        sys.exit(2)

    print('DESTINATION : {}'.format(destination))
    os.chdir(destination)
    Handler = server.SimpleHTTPRequestHandler
    httpd = socketserver.TCPServer(("", port), Handler, False)
    print(" * Running on http://127.0.0.1:{}/".format(port))

    try:
        httpd.allow_reuse_address = True
        httpd.server_bind()
        httpd.server_activate()
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('\nAll done!')