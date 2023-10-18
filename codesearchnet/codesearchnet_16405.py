async def reboot(ip_address):
    """ async function to reboot QTM cameras """
    _, protocol = await asyncio.get_event_loop().create_datagram_endpoint(
        QRebootProtocol,
        local_addr=(ip_address, 0),
        allow_broadcast=True,
        reuse_address=True,
    )

    LOG.info("Sending reboot on %s", ip_address)
    protocol.send_reboot()