def adsSyncAddDeviceNotificationReqEx(
    port, adr, data_name, pNoteAttrib, callback, user_handle=None
):
    # type: (int, AmsAddr, str, NotificationAttrib, Callable, int) -> Tuple[int, int]
    """Add a device notification.

    :param int port: local AMS port as returned by adsPortOpenEx()
    :param pyads.structs.AmsAddr adr: local or remote AmsAddr
    :param string data_name: PLC storage address
    :param pyads.structs.NotificationAttrib pNoteAttrib: notification attributes
    :param callback: Callback function to handle notification
    :param user_handle: User Handle
    :rtype: (int, int)
    :returns: notification handle, user handle

    """
    global callback_store

    if NOTEFUNC is None:
        raise TypeError("Callback function type can't be None")

    adsSyncAddDeviceNotificationReqFct = _adsDLL.AdsSyncAddDeviceNotificationReqEx

    pAmsAddr = ctypes.pointer(adr.amsAddrStruct())
    hnl = adsSyncReadWriteReqEx2(
        port, adr, ADSIGRP_SYM_HNDBYNAME, 0x0, PLCTYPE_UDINT, data_name, PLCTYPE_STRING
    )

    nIndexGroup = ctypes.c_ulong(ADSIGRP_SYM_VALBYHND)
    nIndexOffset = ctypes.c_ulong(hnl)
    attrib = pNoteAttrib.notificationAttribStruct()
    pNotification = ctypes.c_ulong()

    nHUser = ctypes.c_ulong(hnl)
    if user_handle is not None:
        nHUser = ctypes.c_ulong(user_handle)

    adsSyncAddDeviceNotificationReqFct.argtypes = [
        ctypes.c_ulong,
        ctypes.POINTER(SAmsAddr),
        ctypes.c_ulong,
        ctypes.c_ulong,
        ctypes.POINTER(SAdsNotificationAttrib),
        NOTEFUNC,
        ctypes.c_ulong,
        ctypes.POINTER(ctypes.c_ulong),
    ]
    adsSyncAddDeviceNotificationReqFct.restype = ctypes.c_long

    def wrapper(addr, notification, user):
        # type: (AmsAddr, SAdsNotificationHeader, int) -> Callable[[SAdsNotificationHeader, str], None]
        return callback(notification, data_name)

    c_callback = NOTEFUNC(wrapper)
    err_code = adsSyncAddDeviceNotificationReqFct(
        port,
        pAmsAddr,
        nIndexGroup,
        nIndexOffset,
        ctypes.byref(attrib),
        c_callback,
        nHUser,
        ctypes.byref(pNotification),
    )

    if err_code:
        raise ADSError(err_code)
    callback_store[pNotification.value] = c_callback
    return (pNotification.value, hnl)