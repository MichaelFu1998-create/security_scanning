def deploy_services(self, site=None):
        """
        Collects the configurations for all registered services and writes
        the appropriate supervisord.conf file.
        """

        verbose = self.verbose

        r = self.local_renderer
        if not r.env.manage_configs:
            return
#
#         target_sites = self.genv.available_sites_by_host.get(hostname, None)

        self.render_paths()

        supervisor_services = []

        if r.env.purge_all_confs:
            r.sudo('rm -Rf /etc/supervisor/conf.d/*')

        #TODO:check available_sites_by_host and remove dead?
        self.write_configs(site=site)
        for _site, site_data in self.iter_sites(site=site, renderer=self.render_paths):
            if verbose:
                print('deploy_services.site:', _site)

            # Only load site configurations that are allowed for this host.
#             if target_sites is not None:
#                 assert isinstance(target_sites, (tuple, list))
#                 if site not in target_sites:
#                     continue

            for cb in self.genv._supervisor_create_service_callbacks:
                if self.verbose:
                    print('cb:', cb)
                ret = cb(site=_site)
                if self.verbose:
                    print('ret:', ret)
                if isinstance(ret, six.string_types):
                    supervisor_services.append(ret)
                elif isinstance(ret, tuple):
                    assert len(ret) == 2
                    conf_name, conf_content = ret
                    if self.dryrun:
                        print('supervisor conf filename:', conf_name)
                        print(conf_content)
                    self.write_to_file(conf_content)

        self.env.services_rendered = '\n'.join(supervisor_services)

        fn = self.render_to_file(self.env.config_template)
        r.put(local_path=fn, remote_path=self.env.config_path, use_sudo=True)

        # We use supervisorctl to configure supervisor, but this will throw a uselessly vague
        # error message is supervisor isn't running.
        if not self.is_running():
            self.start()

        # Reload config and then add and remove as necessary (restarts programs)
        r.sudo('supervisorctl update')