def install_sql(self, site=None, database='default', apps=None, stop_on_error=0, fn=None):
        """
        Installs all custom SQL.
        """
        #from burlap.db import load_db_set

        stop_on_error = int(stop_on_error)

        site = site or ALL

        name = database

        r = self.local_renderer
        paths = glob.glob(r.format(r.env.install_sql_path_template))

        apps = [_ for _ in (apps or '').split(',') if _.strip()]
        if self.verbose:
            print('install_sql.apps:', apps)

        def cmp_paths(d0, d1):
            if d0[1] and d0[1] in d1[2]:
                return -1
            if d1[1] and d1[1] in d0[2]:
                return +1
            return cmp(d0[0], d1[0])

        def get_paths(t):
            """
            Returns SQL file paths in an execution order that respect dependencies.
            """
            data = [] # [(path, view_name, content)]
            for path in paths:
                if fn and fn not in path:
                    continue
                parts = path.split('.')
                if len(parts) == 3 and parts[1] != t:
                    continue
                if not path.lower().endswith('.sql'):
                    continue
                content = open(path, 'r').read()
                matches = re.findall(r'[\s\t]+VIEW[\s\t]+([a-zA-Z0-9_]{3,})', content, flags=re.IGNORECASE)
                view_name = ''
                if matches:
                    view_name = matches[0]
                    print('Found view %s.' % view_name)
                data.append((path, view_name, content))
            for d in sorted(data, cmp=cmp_paths):
                yield d[0]

        def run_paths(paths, cmd_template, max_retries=3):
            r = self.local_renderer
            paths = list(paths)
            error_counts = defaultdict(int) # {path:count}
            terminal = set()
            if self.verbose:
                print('Checking %i paths.' % len(paths))
            while paths:
                path = paths.pop(0)
                if self.verbose:
                    print('path:', path)
                app_name = re.findall(r'/([^/]+)/sql/', path)[0]
                if apps and app_name not in apps:
                    self.vprint('skipping because app_name %s not in apps' % app_name)
                    continue
                with self.settings(warn_only=True):
                    if self.is_local:
                        r.env.sql_path = path
                    else:
                        r.env.sql_path = '/tmp/%s' % os.path.split(path)[-1]
                        r.put(local_path=path, remote_path=r.env.sql_path)
                    ret = r.run_or_local(cmd_template)
                    if ret and ret.return_code:

                        if stop_on_error:
                            raise Exception('Unable to execute file %s' % path)

                        error_counts[path] += 1
                        if error_counts[path] < max_retries:
                            paths.append(path)
                        else:
                            terminal.add(path)
            if terminal:
                print('%i files could not be loaded.' % len(terminal), file=sys.stderr)
                for path in sorted(list(terminal)):
                    print(path, file=sys.stderr)
                print(file=sys.stderr)

        if self.verbose:
            print('install_sql.db_engine:', r.env.db_engine)

        for _site, site_data in self.iter_sites(site=site, no_secure=True):

            self.set_db(name=name, site=_site)

            if 'postgres' in r.env.db_engine or 'postgis' in r.env.db_engine:
                paths = list(get_paths('postgresql'))
                run_paths(
                    paths=paths,
                    cmd_template="psql --host={db_host} --user={db_user} --no-password -d {db_name} -f {sql_path}")

            elif 'mysql' in r.env.db_engine:
                paths = list(get_paths('mysql'))
                run_paths(
                    paths=paths,
                    cmd_template="mysql -v -h {db_host} -u {db_user} -p'{db_password}' {db_name} < {sql_path}")

            else:
                raise NotImplementedError