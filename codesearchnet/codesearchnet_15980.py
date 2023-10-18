def heartbeat():
    """Call Heartbeat URL"""
    print "We got a call heartbeat notification\n"

    if request.method == 'POST':
        print request.form
    else:
        print request.args

    return "OK"