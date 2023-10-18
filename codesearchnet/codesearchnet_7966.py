def notification(self, plc_datatype=None):
        # type: (Optional[Type[Any]]) -> Callable
        """Decorate a callback function.

        **Decorator**.

        A decorator that can be used for callback functions in order to
        convert the data of the NotificationHeader into the fitting
        Python type.

        :param plc_datatype: The PLC datatype that needs to be converted. This can
        be any basic PLC datatype or a `ctypes.Structure`.

        The callback functions need to be of the following type:

        >>> def callback(handle, name, timestamp, value)

        * `handle`: the notification handle
        * `name`: the variable name
        * `timestamp`: the timestamp as datetime value
        * `value`: the converted value of the variable

        **Usage**:

            >>> import pyads
            >>>
            >>> plc = pyads.Connection('172.18.3.25.1.1', 851)
            >>>
            >>>
            >>> @plc.notification(pyads.PLCTYPE_STRING)
            >>> def callback(handle, name, timestamp, value):
            >>>     print(handle, name, timestamp, value)
            >>>
            >>>
            >>> with plc:
            >>>    attr = pyads.NotificationAttrib(20,
            >>>                                    pyads.ADSTRANS_SERVERCYCLE)
            >>>    handles = plc.add_device_notification('GVL.test', attr,
            >>>                                          callback)
            >>>    while True:
            >>>        pass

        """

        def notification_decorator(func):
            # type: (Callable[[int, str, datetime, Any], None]) -> Callable[[Any, str], None] # noqa: E501

            def func_wrapper(notification, data_name):
                # type: (Any, str) -> None
                contents = notification.contents
                data = contents.data
                data_size = contents.cbSampleSize

                datatype_map = {
                    PLCTYPE_BOOL: "<?",
                    PLCTYPE_BYTE: "<c",
                    PLCTYPE_DINT: "<i",
                    PLCTYPE_DWORD: "<I",
                    PLCTYPE_INT: "<h",
                    PLCTYPE_LREAL: "<d",
                    PLCTYPE_REAL: "<f",
                    PLCTYPE_SINT: "<b",
                    PLCTYPE_UDINT: "<L",
                    PLCTYPE_UINT: "<H",
                    PLCTYPE_USINT: "<B",
                    PLCTYPE_WORD: "<H",
                }  # type: Dict[Type, str]

                if plc_datatype == PLCTYPE_STRING:
                    dest = (c_ubyte * data_size)()
                    memmove(addressof(dest), addressof(data), data_size)
                    # read only until null-termination character
                    value = bytearray(dest).split(b"\0", 1)[0].decode("utf-8")

                elif issubclass(plc_datatype, Structure):
                    value = plc_datatype()
                    fit_size = min(data_size, sizeof(value))
                    memmove(addressof(value), addressof(data), fit_size)

                elif plc_datatype not in datatype_map:
                    value = data

                else:
                    value = struct.unpack(
                        datatype_map[plc_datatype], bytearray(data)[:data_size]
                    )[0]

                dt = filetime_to_dt(contents.nTimeStamp)

                return func(contents.hNotification, data_name, dt, value)

            return func_wrapper

        return notification_decorator