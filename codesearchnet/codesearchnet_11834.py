def deploy(self, site=None):
        """
        Writes entire crontab to the host.
        """
        r = self.local_renderer

        self.deploy_logrotate()

        cron_crontabs = []
#         if self.verbose:
#             print('hostname: "%s"' % (hostname,), file=sys.stderr)
        for _site, site_data in self.iter_sites(site=site):
            r.env.cron_stdout_log = r.format(r.env.stdout_log_template)
            r.env.cron_stderr_log = r.format(r.env.stderr_log_template)
            r.sudo('touch {cron_stdout_log}')
            r.sudo('touch {cron_stderr_log}')
            r.sudo('sudo chown {user}:{user} {cron_stdout_log}')
            r.sudo('sudo chown {user}:{user} {cron_stderr_log}')

            if self.verbose:
                print('site:', site, file=sys.stderr)
                print('env.crontabs_selected:', self.env.crontabs_selected, file=sys.stderr)

            for selected_crontab in self.env.crontabs_selected:
                lines = self.env.crontabs_available.get(selected_crontab, [])
                if self.verbose:
                    print('lines:', lines, file=sys.stderr)
                for line in lines:
                    cron_crontabs.append(r.format(line))

        if not cron_crontabs:
            return

        cron_crontabs = self.env.crontab_headers + cron_crontabs
        cron_crontabs.append('\n')
        r.env.crontabs_rendered = '\n'.join(cron_crontabs)
        fn = self.write_to_file(content=r.env.crontabs_rendered)
        print('fn:', fn)
        r.env.put_remote_path = r.put(local_path=fn)
        if isinstance(r.env.put_remote_path, (tuple, list)):
            r.env.put_remote_path = r.env.put_remote_path[0]
        r.sudo('crontab -u {cron_user} {put_remote_path}')