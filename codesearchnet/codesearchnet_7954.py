def add_device_notification(adr, data_name, attr, callback, user_handle=None):
    # type: (AmsAddr, str, NotificationAttrib, Callable, int) -> Optional[Tuple[int, int]]  # noqa: E501
    """Add a device notification.

    :param pyads.structs.AmsAddr adr: AMS Address associated with the routing
        entry which is to be removed from the router.
    :param str data_name: PLC storage address
    :param pyads.structs.NotificationAttrib attr: object that contains
        all the attributes for the definition of a notification
    :param callback: callback function that gets executed on in the event
        of a notification

    :rtype: (int, int)
    :returns: notification handle, user handle

    Save the notification handle and the user handle on creating a
    notification if you want to be able to remove the notification
    later in your code.

    """
    if port is not None:
        return adsSyncAddDeviceNotificationReqEx(
            port, adr, data_name, attr, callback, user_handle
        )

    return None