async def packet_receiver(queue):
    """ Asynchronous function that processes queue until None is posted in queue """
    LOG.info("Entering packet_receiver")
    while True:
        packet = await queue.get()
        if packet is None:
            break

        LOG.info("Framenumber %s", packet.framenumber)
    LOG.info("Exiting packet_receiver")