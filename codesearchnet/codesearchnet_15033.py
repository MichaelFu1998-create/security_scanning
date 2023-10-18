def _to_webdav(self, docs_base, release):
        """Upload to WebDAV store."""
        try:
            git_path = subprocess.check_output('git remote get-url origin 2>/dev/null', shell=True)
        except subprocess.CalledProcessError:
            git_path = ''
        else:
            git_path = git_path.decode('ascii').strip()
            git_path = git_path.replace('http://', '').replace('https://', '').replace('ssh://', '')
            git_path = re.search(r'[^:/]+?[:/](.+)', git_path)
            git_path = git_path.group(1).replace('.git', '') if git_path else ''
        url = None
        with self._zipped(docs_base) as handle:
            url_ns = dict(name=self.cfg.project.name, version=release, git_path=git_path)
            reply = requests.put(self.params['url'].format(**url_ns),
                                 data=handle.read(), headers={'Accept': 'application/json'})
            if reply.status_code in range(200, 300):
                notify.info("{status_code} {reason}".format(**vars(reply)))
                try:
                    data = reply.json()
                except ValueError as exc:
                    notify.warning("Didn't get a JSON response! ({})".format(exc))
                else:
                    if 'downloadUri' in data:  # Artifactory
                        url = data['downloadUri'] + '!/index.html'
            elif reply.status_code == 301:
                url = reply.headers['location']
            else:
                data = self.cfg.copy()
                data.update(self.params)
                data.update(vars(reply))
                notify.error("{status_code} {reason} for PUT to {url}".format(**data))

        if not url:
            notify.warning("Couldn't get URL from upload response!")
        return url