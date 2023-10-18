def on_interrupt(handler, reraise=False):
    """
    context for handling keyboardinterrupt
    ex)
    with on_interrupt(handler):
        critical_work_to_prevent()

    from logger import logg
    on_interrupt.signal = None

    :param function handler:
    :param bool reraise:
    :return: context
    """

    def _handler(sig, frame):
        handler.signal = (sig, frame)
        handler._reraise = handler()

    handler._reraise = False
    handler.signal = None
    oldhandler = signal.getsignal(signal.SIGINT)
    signal.signal(signal.SIGINT, _handler)

    yield handler

    signal.signal(signal.SIGINT, oldhandler)
    if (reraise or handler._reraise) and handler.signal:
        oldhandler(*handler.signal)