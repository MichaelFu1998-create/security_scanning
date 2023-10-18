def CherryPyWSGIServer(bind_addr,
                       wsgi_app,
                       numthreads = 10,
                       server_name = None,
                       max = -1,
                       request_queue_size = 5,
                       timeout = 10,
                       shutdown_timeout = 5):
    """ A Cherrypy wsgiserver-compatible wrapper. """
    max_threads = max
    if max_threads < 0:
        max_threads = 0
    return Rocket(bind_addr, 'wsgi', {'wsgi_app': wsgi_app},
                  min_threads = numthreads,
                  max_threads = max_threads,
                  queue_size = request_queue_size,
                  timeout = timeout)