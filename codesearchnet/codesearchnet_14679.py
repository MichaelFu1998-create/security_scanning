def terminal(port=default_port(), baud='9600'):
    """Launch minterm from pyserial"""
    testargs = ['nodemcu-uploader', port, baud]
    # TODO: modifying argv is no good
    sys.argv = testargs
    # resuse miniterm on main function
    miniterm.main()