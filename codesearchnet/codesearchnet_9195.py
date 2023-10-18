def find_ports(device):
    """
    Find the port chain a device is plugged on.

    This is done by searching sysfs for a device that matches the device
    bus/address combination.

    Useful when the underlying usb lib does not return device.port_number for
    whatever reason.
    """
    bus_id = device.bus
    dev_id = device.address
    for dirent in os.listdir(USB_SYS_PREFIX):
        matches = re.match(USB_PORTS_STR + '$', dirent)
        if matches:
            bus_str = readattr(dirent, 'busnum')
            if bus_str:
                busnum = float(bus_str)
            else:
                busnum = None
            dev_str = readattr(dirent, 'devnum')
            if dev_str:
                devnum = float(dev_str)
            else:
                devnum = None
            if busnum == bus_id and devnum == dev_id:
                return str(matches.groups()[1])