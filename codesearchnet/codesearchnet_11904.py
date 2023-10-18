def record_manifest(self):
        """
        Called after a deployment to record any data necessary to detect changes
        for a future deployment.
        """
        data = super(SupervisorSatchel, self).record_manifest()

        # Celery deploys itself through supervisor, so monitor its changes too in Apache site configs.
        for site_name, site_data in self.genv.sites.items():
            if self.verbose:
                print(site_name, site_data)
            data['celery_has_worker_%s' % site_name] = site_data.get('celery_has_worker', False)

        data['configured'] = True

        # Generate services list.
        self.write_configs(upload=0)
        #data['services_rendered'] = ''

        return data