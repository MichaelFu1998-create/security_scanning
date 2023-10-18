def tunnel(self, local_port, remote_port):
        """
        Creates an SSH tunnel.
        """
        r = self.local_renderer
        r.env.tunnel_local_port = local_port
        r.env.tunnel_remote_port = remote_port
        r.local(' ssh -i {key_filename} -L {tunnel_local_port}:localhost:{tunnel_remote_port} {user}@{host_string} -N')