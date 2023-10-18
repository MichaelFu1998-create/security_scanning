def getch():
    """
    get character. waiting for key
    """
    try:
        termios.tcsetattr(_fd, termios.TCSANOW, _new_settings)
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(_fd, termios.TCSADRAIN, _old_settings)
    return ch