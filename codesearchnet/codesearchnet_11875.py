def fix_eth0_rename(self, hardware_addr):
        """
        A bug as of 2016.10.10 causes eth0 to be renamed to enx*.
        This renames it to eth0.

        http://raspberrypi.stackexchange.com/q/43560/29103
        """
        r = self.local_renderer
        r.env.hardware_addr = hardware_addr
        r.sudo('ln -s /dev/null /etc/udev/rules.d/80-net-name-slot.rules')
        r.append(
            text=r'SUBSYSTEM=="net", ACTION=="add", DRIVERS=="?*", '\
                r'ATTR\{address\}=="{hardware_addr}", '\
                r'ATTR\{dev_id\}=="0x0", '\
                r'ATTR\{type\}=="1", '\
                r'KERNEL=="eth*", NAME="eth0"',
            filename='/etc/udev/rules.d/70-persistent-net.rules',
            use_sudo=True,
        )