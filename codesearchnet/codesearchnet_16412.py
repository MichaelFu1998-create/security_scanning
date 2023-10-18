async def choose_qtm_instance(interface):
    """ List running QTM instances, asks for input and return chosen QTM """
    instances = {}
    print("Available QTM instances:")
    async for i, qtm_instance in AsyncEnumerate(qtm.Discover(interface), start=1):
        instances[i] = qtm_instance
        print("{} - {}".format(i, qtm_instance.info))

    try:

        choice = int(input("Connect to: "))

        if choice not in instances:
            raise ValueError

    except ValueError:
        LOG.error("Invalid choice")
        return None

    return instances[choice].host