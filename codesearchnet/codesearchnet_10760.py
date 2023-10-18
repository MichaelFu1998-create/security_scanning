def available_devices():
    """
    Display available input and output audio devices along with their
    port indices.

    :return:  Dictionary whose keys are the device index, the number of inputs and outputs, and their names.
    :rtype: dict
    """
    devices = {}
    pA = pyaudio.PyAudio()
    device_string = str()
    for k in range(pA.get_device_count()):
        dev = pA.get_device_info_by_index(k)
        devices[k] = {'name': dev['name'], 'inputs': dev['maxInputChannels'], 'outputs': dev['maxOutputChannels']}
        device_string += 'Index %d device name = %s, inputs = %d, outputs = %d\n' % \
                        (k,dev['name'],dev['maxInputChannels'],dev['maxOutputChannels'])
    logger.debug(device_string)
    return devices