def initialize(self):
        """Initialize bluez DBus communication.  Must be called before any other
        calls are made!
        """
        # Ensure GLib's threading is initialized to support python threads, and
        # make a default mainloop that all DBus objects will inherit.  These
        # commands MUST execute before any other DBus commands!
        GObject.threads_init()
        dbus.mainloop.glib.threads_init()
        # Set the default main loop, this also MUST happen before other DBus calls.
        self._mainloop = dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
        # Get the main DBus system bus and root bluez object.
        self._bus = dbus.SystemBus()
        self._bluez = dbus.Interface(self._bus.get_object('org.bluez', '/'),
                                     'org.freedesktop.DBus.ObjectManager')