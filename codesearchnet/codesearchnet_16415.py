async def setup():
    """ main function """

    connection = await qtm.connect("127.0.0.1")

    if connection is None:
        return -1

    async with qtm.TakeControl(connection, "password"):

        state = await connection.get_state()
        if state != qtm.QRTEvent.EventConnected:
            await connection.new()
            try:
                await connection.await_event(qtm.QRTEvent.EventConnected, timeout=10)
            except asyncio.TimeoutError:
                LOG.error("Failed to start new measurement")
                return -1

        queue = asyncio.Queue()

        receiver_future = asyncio.ensure_future(package_receiver(queue))

        await connection.stream_frames(components=["2d"], on_packet=queue.put_nowait)

        asyncio.ensure_future(shutdown(30, connection, receiver_future, queue))