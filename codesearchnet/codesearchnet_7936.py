def adsSyncReadDeviceInfoReqEx(port, address):
    # type: (int, AmsAddr) -> Tuple[str, AdsVersion]
    """Read the name and the version number of the ADS-server.

    :param int port: local AMS port as returned by adsPortOpenEx()
    :param pyads.structs.AmsAddr address: local or remote AmsAddr
    :rtype: string, AdsVersion
    :return: device name, version

    """
    sync_read_device_info_request = _adsDLL.AdsSyncReadDeviceInfoReqEx

    # Get pointer to the target AMS address
    ams_address_pointer = ctypes.pointer(address.amsAddrStruct())

    # Create buffer to be filled with device name, get pointer to said buffer
    device_name_buffer = ctypes.create_string_buffer(20)
    device_name_pointer = ctypes.pointer(device_name_buffer)

    # Create ADS Version struct and get pointer.
    ads_version = SAdsVersion()
    ads_version_pointer = ctypes.pointer(ads_version)

    error_code = sync_read_device_info_request(
        port, ams_address_pointer, device_name_pointer, ads_version_pointer
    )

    if error_code:
        raise ADSError(error_code)

    return (device_name_buffer.value.decode(), AdsVersion(ads_version))