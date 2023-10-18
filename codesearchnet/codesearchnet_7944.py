def adsSyncDelDeviceNotificationReqEx(port, adr, notification_handle, user_handle):
    # type: (int, AmsAddr, int, int) -> None
    """Remove a device notification.

    :param int port: local AMS port as returned by adsPortOpenEx()
    :param pyads.structs.AmsAddr adr: local or remote AmsAddr
    :param int notification_handle: Notification Handle
    :param int user_handle: User Handle

    """
    adsSyncDelDeviceNotificationReqFct = _adsDLL.AdsSyncDelDeviceNotificationReqEx

    pAmsAddr = ctypes.pointer(adr.amsAddrStruct())
    nHNotification = ctypes.c_ulong(notification_handle)
    err_code = adsSyncDelDeviceNotificationReqFct(port, pAmsAddr, nHNotification)
    callback_store.pop(notification_handle, None)
    if err_code:
        raise ADSError(err_code)

    adsSyncWriteReqEx(port, adr, ADSIGRP_SYM_RELEASEHND, 0, user_handle, PLCTYPE_UDINT)