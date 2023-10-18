def database_renderer(self, name=None, site=None, role=None):
        """
        Renders local settings for a specific database.
        """

        name = name or self.env.default_db_name

        site = site or self.genv.SITE

        role = role or self.genv.ROLE

        key = (name, site, role)
        self.vprint('checking key:', key)
        if key not in self._database_renderers:
            self.vprint('No cached db renderer, generating...')

            if self.verbose:
                print('db.name:', name)
                print('db.databases:', self.env.databases)
                print('db.databases[%s]:' % name, self.env.databases.get(name))

            d = type(self.genv)(self.lenv)
            d.update(self.get_database_defaults())
            d.update(self.env.databases.get(name, {}))
            d['db_name'] = name
            if self.verbose:
                print('db.d:')
                pprint(d, indent=4)
                print('db.connection_handler:', d.connection_handler)

            if d.connection_handler == CONNECTION_HANDLER_DJANGO:
                self.vprint('Using django handler...')
                dj = self.get_satchel('dj')
                if self.verbose:
                    print('Loading Django DB settings for site {} and role {}.'.format(site, role), file=sys.stderr)
                dj.set_db(name=name, site=site, role=role)
                _d = dj.local_renderer.collect_genv(include_local=True, include_global=False)

                # Copy "dj_db_*" into "db_*".
                for k, v in _d.items():
                    if k.startswith('dj_db_'):
                        _d[k[3:]] = v
                    del _d[k]

                if self.verbose:
                    print('Loaded:')
                    pprint(_d)
                d.update(_d)

            elif d.connection_handler and d.connection_handler.startswith(CONNECTION_HANDLER_CUSTOM+':'):

                _callable_str = d.connection_handler[len(CONNECTION_HANDLER_CUSTOM+':'):]
                self.vprint('Using custom handler %s...' % _callable_str)
                _d = str_to_callable(_callable_str)(role=self.genv.ROLE)
                if self.verbose:
                    print('Loaded:')
                    pprint(_d)
                d.update(_d)

            r = LocalRenderer(self, lenv=d)

            # Optionally set any root logins needed for administrative commands.
            self.set_root_login(r)

            self._database_renderers[key] = r
        else:
            self.vprint('Cached db renderer found.')

        return self._database_renderers[key]