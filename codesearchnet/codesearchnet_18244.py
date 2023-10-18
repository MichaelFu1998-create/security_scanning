def mongo(daemon=False, port=20771):
    '''Run the mongod process.
    '''
    cmd = "mongod --port {0}".format(port)
    if daemon:
        cmd += " --fork"
    run(cmd)