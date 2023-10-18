def manage(self, cmd, *args, **kwargs):
        """
        A generic wrapper around Django's manage command.
        """
        r = self.local_renderer
        environs = kwargs.pop('environs', '').strip()
        if environs:
            environs = ' '.join('export %s=%s;' % tuple(_.split('=')) for _ in environs.split(','))
            environs = ' ' + environs + ' '
        r.env.cmd = cmd
        r.env.SITE = r.genv.SITE or r.genv.default_site
        r.env.args = ' '.join(map(str, args))
        r.env.kwargs = ' '.join(
            ('--%s' % _k if _v in (True, 'True') else '--%s=%s' % (_k, _v))
            for _k, _v in kwargs.items())
        r.env.environs = environs
        if self.is_local:
            r.env.project_dir = r.env.local_project_dir
        r.run_or_local('export SITE={SITE}; export ROLE={ROLE};{environs} cd {project_dir}; {manage_cmd} {cmd} {args} {kwargs}')