def die(msg, code=-1):
    """Writes msg to stderr and exits with return code"""
    sys.stderr.write(msg + "\n")
    sys.exit(code)