def maint_up(self):
        """
        Forwards all traffic to a page saying the server is down for maintenance.
        """
        r = self.local_renderer
        fn = self.render_to_file(r.env.maintenance_template, extra={'current_hostname': self.current_hostname})
        r.put(local_path=fn, remote_path=r.env.maintenance_path, use_sudo=True)
        r.sudo('chown -R {apache_web_user}:{apache_web_group} {maintenance_path}')