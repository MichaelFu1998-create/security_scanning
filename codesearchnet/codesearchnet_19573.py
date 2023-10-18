def interrupt_guard(msg='', reraise=True):
    """
    context for guard keyboardinterrupt
    ex)
    with interrupt_guard('need long time'):
        critical_work_to_prevent()

    :param str msg: message to print when interrupted
    :param reraise: re-raise or not when exit
    :return: context
    """
    def echo():
        print(msg)

    return on_interrupt(echo, reraise=reraise)