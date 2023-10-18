def configure_hdmi(self):
        """
        Configures HDMI to support hot-plugging, so it'll work even if it wasn't
        plugged in when the Pi was originally powered up.

        Note, this does cause slightly higher power consumption, so if you don't need HDMI,
        don't bother with this.

        http://raspberrypi.stackexchange.com/a/2171/29103
        """
        r = self.local_renderer

        # use HDMI mode even if no HDMI monitor is detected
        r.enable_attr(
            filename='/boot/config.txt',
            key='hdmi_force_hotplug',
            value=1,
            use_sudo=True,
        )

        # to normal HDMI mode (Sound will be sent if supported and enabled). Without this line,
        # the Raspbmc would switch to DVI (with no audio) mode by default.
        r.enable_attr(
            filename='/boot/config.txt',
            key='hdmi_drive',
            value=2,
            use_sudo=True,
        )