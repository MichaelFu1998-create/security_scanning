def del_device_notification(adr, notification_handle, user_handle):
    # type: (AmsAddr, int, int) -> None
    """Remove a device notification.

    :param pyads.structs.AmsAddr adr: AMS Address associated with the routing
        entry which is to be removed from the router.
    :param notification_handle: address of the variable that contains
        the handle of the notification
    :param user_handle: user handle

    """
    if port is not None:
        return adsSyncDelDeviceNotificationReqEx(
            port, adr, notification_handle, user_handle
        )