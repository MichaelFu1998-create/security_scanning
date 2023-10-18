async def main(interface=None):
    """ Main function """

    qtm_ip = await choose_qtm_instance(interface)
    if qtm_ip is None:
        return

    while True:

        connection = await qtm.connect(qtm_ip, 22223, version="1.18")

        if connection is None:
            return

        await connection.get_state()
        await connection.byte_order()

        async with qtm.TakeControl(connection, "password"):

            result = await connection.close()
            if result == b"Closing connection":
                await connection.await_event(qtm.QRTEvent.EventConnectionClosed)

            await connection.load(QTM_FILE)

            await connection.start(rtfromfile=True)

            (await connection.get_current_frame()).get_3d_markers()

            queue = asyncio.Queue()

            asyncio.ensure_future(packet_receiver(queue))

            try:
                await connection.stream_frames(
                    components=["incorrect"], on_packet=queue.put_nowait
                )
            except qtm.QRTCommandException as exception:
                LOG.info("exception %s", exception)

            await connection.stream_frames(
                components=["3d"], on_packet=queue.put_nowait
            )

            await asyncio.sleep(0.5)
            await connection.byte_order()
            await asyncio.sleep(0.5)
            await connection.stream_frames_stop()
            queue.put_nowait(None)

            await connection.get_parameters(parameters=["3d"])
            await connection.stop()

            await connection.await_event()

            await connection.new()
            await connection.await_event(qtm.QRTEvent.EventConnected)

            await connection.start()
            await connection.await_event(qtm.QRTEvent.EventWaitingForTrigger)

            await connection.trig()
            await connection.await_event(qtm.QRTEvent.EventCaptureStarted)

            await asyncio.sleep(0.5)

            await connection.set_qtm_event()
            await asyncio.sleep(0.001)
            await connection.set_qtm_event("with_label")

            await asyncio.sleep(0.5)

            await connection.stop()
            await connection.await_event(qtm.QRTEvent.EventCaptureStopped)

            await connection.save(r"measurement.qtm")

            await asyncio.sleep(3)

            await connection.close()

        connection.disconnect()