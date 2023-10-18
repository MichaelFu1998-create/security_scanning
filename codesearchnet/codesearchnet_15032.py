def _to_pypi(self, docs_base, release):
        """Upload to PyPI."""
        url = None
        with self._zipped(docs_base) as handle:
            reply = requests.post(self.params['url'], auth=get_pypi_auth(), allow_redirects=False,
                                  files=dict(content=(self.cfg.project.name + '.zip', handle, 'application/zip')),
                                  data={':action': 'doc_upload', 'name': self.cfg.project.name})
            if reply.status_code in range(200, 300):
                notify.info("{status_code} {reason}".format(**vars(reply)))
            elif reply.status_code == 301:
                url = reply.headers['location']
            else:
                data = self.cfg.copy()
                data.update(self.params)
                data.update(vars(reply))
                notify.error("{status_code} {reason} for POST to {url}".format(**data))
        return url