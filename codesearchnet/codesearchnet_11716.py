def static(self):
        """
        Configures the server to use a static IP.
        """
        fn = self.render_to_file('ip/ip_interfaces_static.template')
        r = self.local_renderer
        r.put(local_path=fn, remote_path=r.env.interfaces_fn, use_sudo=True)