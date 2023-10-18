async def connect(
    host,
    port=22223,
    version="1.19",
    on_event=None,
    on_disconnect=None,
    timeout=5,
    loop=None,
) -> QRTConnection:
    """Async function to connect to QTM

    :param host: Address of the computer running QTM.
    :param port: Port number to connect to, should be the port configured for little endian.
    :param version: What version of the protocol to use, tested for 1.17 and above but could
        work with lower versions as well.
    :param on_disconnect: Function to be called when a disconnect from QTM occurs.
    :param on_event: Function to be called when there's an event from QTM.
    :param timeout: The default timeout time for calls to QTM.
    :param loop: Alternative event loop, will use asyncio default if None.

    :rtype: A :class:`.QRTConnection`
    """
    loop = loop or asyncio.get_event_loop()

    try:
        _, protocol = await loop.create_connection(
            lambda: QTMProtocol(
                loop=loop, on_event=on_event, on_disconnect=on_disconnect
            ),
            host,
            port,
        )
    except (ConnectionRefusedError, TimeoutError, OSError) as exception:
        LOG.error(exception)
        return None

    try:
        await protocol.set_version(version)
    except QRTCommandException as exception:
        LOG.error(Exception)
        return None
    except TypeError as exception:  # TODO: fix test requiring this (test_connect_set_version)
        LOG.error(exception)
        return None

    return QRTConnection(protocol, timeout=timeout)