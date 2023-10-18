def _get_repo_info(self, environ, rev, reload=False):
        """Return a dictionary containing all files under source control.

        dirinfos:
            Dictionary containing direct members for every collection.
            {folderpath: (collectionlist, filelist), ...}
        files:
            Sorted list of all file paths in the manifest.
        filedict:
            Dictionary containing all files under source control.

        ::

            {'dirinfos': {'': (['wsgidav',
                                'tools',
                                'WsgiDAV.egg-info',
                                'tests'],
                               ['index.rst',
                                'wsgidav MAKE_DAILY_BUILD.launch',
                                'wsgidav run_server.py DEBUG.launch',
                                'wsgidav-paste.conf',
                                ...
                                'setup.py']),
                          'wsgidav': (['addons', 'samples', 'server', 'interfaces'],
                                      ['__init__.pyc',
                                       'dav_error.pyc',
                                       'dav_provider.pyc',
                                       ...
                                       'wsgidav_app.py']),
                           },
             'files': ['.hgignore',
                       'ADDONS.txt',
                       'wsgidav/samples/mysql_dav_provider.py',
                       ...
                       ],
             'filedict': {'.hgignore': True,
                           'README.txt': True,
                           'WsgiDAV.egg-info/PKG-INFO': True,
                           }
                           }
        """
        caches = environ.setdefault("wsgidav.hg.cache", {})
        if caches.get(compat.to_native(rev)) is not None:
            _logger.debug("_get_repo_info(%s): cache hit." % rev)
            return caches[compat.to_native(rev)]

        start_time = time.time()
        self.ui.pushbuffer()
        commands.manifest(self.ui, self.repo, rev)
        res = self.ui.popbuffer()
        files = []
        dirinfos = {}
        filedict = {}
        for file in res.split("\n"):
            if file.strip() == "":
                continue
            file = file.replace("\\", "/")
            # add all parent directories to 'dirinfos'
            parents = file.split("/")
            if len(parents) >= 1:
                p1 = ""
                for i in range(0, len(parents) - 1):
                    p2 = parents[i]
                    dir = dirinfos.setdefault(p1, ([], []))
                    if p2 not in dir[0]:
                        dir[0].append(p2)
                    if p1 == "":
                        p1 = p2
                    else:
                        p1 = "%s/%s" % (p1, p2)
                dirinfos.setdefault(p1, ([], []))[1].append(parents[-1])
            filedict[file] = True
        files.sort()

        cache = {"files": files, "dirinfos": dirinfos, "filedict": filedict}
        caches[compat.to_native(rev)] = cache
        _logger.info("_getRepoInfo(%s) took %.3f" % (rev, time.time() - start_time))
        return cache