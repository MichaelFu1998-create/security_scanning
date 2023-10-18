def add_device_notification(self, data_name, attr, callback, user_handle=None):
        # type: (str, NotificationAttrib, Callable, int) -> Optional[Tuple[int, int]]
        """Add a device notification.

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

        **Usage**:

            >>> import pyads
            >>> from ctypes import size_of
            >>>
            >>> # Connect to the local TwinCAT PLC
            >>> plc = pyads.Connection('127.0.0.1.1.1', 851)
            >>>
            >>> # Create callback function that prints the value
            >>> def mycallback(adr, notification, user):
            >>>     contents = notification.contents
            >>>     value = next(
            >>>         map(int,
            >>>             bytearray(contents.data)[0:contents.cbSampleSize])
            >>>     )
            >>>     print(value)
            >>>
            >>> with plc:
            >>>     # Add notification with default settings
            >>>     attr = pyads.NotificationAttrib(size_of(pyads.PLCTYPE_INT))
            >>>
            >>>     hnotification, huser = plc.add_device_notification(
            >>>         adr, attr, mycallback)
            >>>
            >>>     # Remove notification
            >>>     plc.del_device_notification(hnotification, huser)

        """
        if self._port is not None:
            notification_handle, user_handle = adsSyncAddDeviceNotificationReqEx(
                self._port, self._adr, data_name, attr, callback, user_handle
            )
            return notification_handle, user_handle

        return None