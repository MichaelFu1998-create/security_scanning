def main(port=4118, parentpid=None):
    """Main entry point. Parse command line options and start up a server."""
    if "LDTP_DEBUG" in os.environ:
        _ldtp_debug = True
    else:
        _ldtp_debug = False
    _ldtp_debug_file = os.environ.get('LDTP_DEBUG_FILE', None)
    if _ldtp_debug:
        print("Parent PID: {}".format(int(parentpid)))
    if _ldtp_debug_file:
        with open(unicode(_ldtp_debug_file), "a") as fp:
            fp.write("Parent PID: {}".format(int(parentpid)))
    server = LDTPServer(('', port), allow_none=True, logRequests=_ldtp_debug,
                        requestHandler=RequestHandler)
    server.register_introspection_functions()
    server.register_multicall_functions()
    ldtp_inst = core.Core()
    server.register_instance(ldtp_inst)
    if parentpid:
        thread.start_new_thread(notifyclient, (parentpid,))
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    except:
        if _ldtp_debug:
            print(traceback.format_exc())
        if _ldtp_debug_file:
            with open(_ldtp_debug_file, "a") as fp:
                fp.write(traceback.format_exc())