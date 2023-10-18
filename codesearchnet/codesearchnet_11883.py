def fix_lsmod_for_pi3(self):
        """
        Some images purporting to support both the Pi2 and Pi3 use the wrong kernel modules.
        """
        r = self.local_renderer
        r.env.rpi2_conf = '/etc/modules-load.d/rpi2.conf'
        r.sudo("sed '/bcm2808_rng/d' {rpi2_conf}")
        r.sudo("echo bcm2835_rng >> {rpi2_conf}")