def get_settings(self, site=None, role=None):
        """
        Retrieves the Django settings dictionary.
        """
        r = self.local_renderer
        _stdout = sys.stdout
        _stderr = sys.stderr
        if not self.verbose:
            sys.stdout = StringIO()
            sys.stderr = StringIO()
        try:
            sys.path.insert(0, r.env.src_dir)

            # Temporarily override SITE.
            tmp_site = self.genv.SITE
            if site and site.endswith('_secure'):
                site = site[:-7]
            site = site or self.genv.SITE or self.genv.default_site
            self.set_site(site)

            # Temporarily override ROLE.
            tmp_role = self.genv.ROLE
            if role:
                self.set_role(role)

            try:
                # We need to explicitly delete sub-modules from sys.modules. Otherwise, reload() skips
                # them and they'll continue to contain obsolete settings.
                if r.env.delete_module_with_prefixes:
                    for name in sorted(sys.modules):
                        for prefix in r.env.delete_module_with_prefixes:
                            if name.startswith(prefix):
                                if self.verbose:
                                    print('Deleting module %s prior to re-import.' % name)
                                del sys.modules[name]
                                break

                for name in list(sys.modules):
                    for s in r.env.delete_module_containing:
                        if s in name:
                            del sys.modules[name]
                            break

                if r.env.settings_module in sys.modules:
                    del sys.modules[r.env.settings_module]

                #TODO:fix r.env.settings_module not loading from settings?
#                 print('r.genv.django_settings_module:', r.genv.django_settings_module, file=_stdout)
#                 print('r.genv.dj_settings_module:', r.genv.dj_settings_module, file=_stdout)
#                 print('r.env.settings_module:', r.env.settings_module, file=_stdout)
                if 'django_settings_module' in r.genv:
                    r.env.settings_module = r.genv.django_settings_module
                else:
                    r.env.settings_module = r.env.settings_module or r.genv.dj_settings_module
                if self.verbose:
                    print('r.env.settings_module:', r.env.settings_module, r.format(r.env.settings_module))
                module = import_module(r.format(r.env.settings_module))

                if site:
                    assert site == module.SITE, 'Unable to set SITE to "%s" Instead it is set to "%s".' % (site, module.SITE)

                # Works as long as settings.py doesn't also reload anything.
                import imp
                imp.reload(module)

            except ImportError as e:
                print('Warning: Could not import settings for site "%s": %s' % (site, e), file=_stdout)
                traceback.print_exc(file=_stdout)
                #raise # breaks *_secure pseudo sites
                return
            finally:
                if tmp_site:
                    self.set_site(tmp_site)
                if tmp_role:
                    self.set_role(tmp_role)
        finally:
            sys.stdout = _stdout
            sys.stderr = _stderr
            sys.path.remove(r.env.src_dir)
        return module