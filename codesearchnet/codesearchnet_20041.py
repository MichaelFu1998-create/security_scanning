async def _try_catch_coro(emitter, event, listener, coro):
    """Coroutine wrapper to catch errors after async scheduling.

    Args:
        emitter (EventEmitter): The event emitter that is attempting to
            call a listener.
        event (str): The event that triggered the emitter.
        listener (async def): The async def that was used to generate the coro.
        coro (coroutine): The coroutine that should be tried.

    If an exception is caught the function will use the emitter to emit the
    failure event. If, however, the current event _is_ the failure event then
    the method reraises. The reraised exception may show in debug mode for the
    event loop but is otherwise silently dropped.
    """
    try:

        await coro

    except Exception as exc:

        if event == emitter.LISTENER_ERROR_EVENT:

            raise

        emitter.emit(emitter.LISTENER_ERROR_EVENT, event, listener, exc)