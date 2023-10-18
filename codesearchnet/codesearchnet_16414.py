async def package_receiver(queue):
    """ Asynchronous function that processes queue until None is posted in queue """
    LOG.info("Entering package_receiver")
    while True:
        packet = await queue.get()
        if packet is None:
            break

        LOG.info("Framenumber %s", packet.framenumber)
        header, cameras = packet.get_2d_markers()
        LOG.info("Component info: %s", header)

        for i, camera in enumerate(cameras, 1):
            LOG.info("Camera %d", i)
            for marker in camera:
                LOG.info("\t%s", marker)

    LOG.info("Exiting package_receiver")