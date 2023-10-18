def manage_async(self, command='', name='process', site=ALL, exclude_sites='', end_message='', recipients=''):
        """
        Starts a Django management command in a screen.

        Parameters:

            command :- all arguments passed to `./manage` as a single string

            site :- the site to run the command for (default is all)

        Designed to be ran like:

            fab <role> dj.manage_async:"some_management_command --force"

        """
        exclude_sites = exclude_sites.split(':')
        r = self.local_renderer
        for _site, site_data in self.iter_sites(site=site, no_secure=True):
            if _site in exclude_sites:
                continue
            r.env.SITE = _site
            r.env.command = command
            r.env.end_email_command = ''
            r.env.recipients = recipients or ''
            r.env.end_email_command = ''
            if end_message:
                end_message = end_message + ' for ' + _site
                end_message = end_message.replace(' ', '_')
                r.env.end_message = end_message
                r.env.end_email_command = r.format('{manage_cmd} send_mail --subject={end_message} --recipients={recipients}')
            r.env.name = name.format(**r.genv)
            r.run(
                'screen -dmS {name} bash -c "export SITE={SITE}; '\
                'export ROLE={ROLE}; cd {project_dir}; '\
                '{manage_cmd} {command} --traceback; {end_email_command}"; sleep 3;')