def _run_server():
    """
    Run the image server. This is blocking. Will handle user KeyboardInterrupt
    and other exceptions appropriately and return control once the server is
    stopped.
    @return {None}
    """
    # Get the port to run on
    port = _get_server_port()
    # Configure allow_reuse_address to make re-runs of the script less painful -
    # if this is not True then waiting for the address to be freed after the
    # last run can block a subsequent run
    SocketServer.TCPServer.allow_reuse_address = True
    # Create the server instance
    server = SocketServer.TCPServer(
        ('', port),
        SimpleHTTPServer.SimpleHTTPRequestHandler
    )
    # Print out before actually running the server (cheeky / optimistic, however
    # you want to look at it)
    print('Your images are at http://127.0.0.1:%d/%s' % (
        port,
        INDEX_FILE_NAME
    ))
    # Try to run the server
    try:
        # Run it - this call blocks until the server is killed
        server.serve_forever()
    except KeyboardInterrupt:
        # This is the expected way of the server being killed, since imageMe is
        # intended for ad-hoc running from command line
        print('User interrupted, stopping')
    except Exception as exptn:
        # Catch everything else - this will handle shutdowns via other signals
        # and faults actually starting the server in the first place
        print(exptn)
        print('Unhandled exception in server, stopping')