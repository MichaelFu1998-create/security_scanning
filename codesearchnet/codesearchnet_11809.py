def record_manifest(self):
        """
        Returns a dictionary representing a serialized state of the service.
        """
        manifest = get_component_settings(prefixes=[self.name])

        # Record a signature of each template so we know to redeploy when they change.
        for template in self.get_templates():
            # Dereference brace notation. e.g. convert '{var}' to `env[var]`.
            if template and template.startswith('{') and template.endswith('}'):
                template = self.env[template[1:-1]]

            if not template:
                continue

            if template.startswith('%s/' % self.name):
                fqfn = self.find_template(template)
            else:
                fqfn = self.find_template('%s/%s' % (self.name, template))
            assert fqfn, 'Unable to find template: %s/%s' % (self.name, template)
            manifest['_%s' % template] = get_file_hash(fqfn)

        for tracker in self.get_trackers():
            manifest['_tracker_%s' % tracker.get_natural_key_hash()] = tracker.get_thumbprint()

        if self.verbose:
            pprint(manifest, indent=4)

        return manifest