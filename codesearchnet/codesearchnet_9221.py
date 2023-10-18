def __upload_title(self, kibiter_major):
        """Upload to Kibiter the title for the dashboard.

        The title is shown on top of the dashboard menu, and is Usually
        the name of the project being dashboarded.
        This is done only for Kibiter 6.x.

        :param kibiter_major: major version of kibiter
        """

        if kibiter_major == "6":
            resource = ".kibana/doc/projectname"
            data = {"projectname": {"name": self.project_name}}
            mapping_resource = ".kibana/_mapping/doc"
            mapping = {"dynamic": "true"}

            url = urijoin(self.conf['es_enrichment']['url'], resource)
            mapping_url = urijoin(self.conf['es_enrichment']['url'],
                                  mapping_resource)

            logger.debug("Adding mapping for dashboard title")
            res = self.grimoire_con.put(mapping_url, data=json.dumps(mapping),
                                        headers=ES6_HEADER)
            try:
                res.raise_for_status()
            except requests.exceptions.HTTPError:
                logger.error("Couldn't create mapping for dashboard title.")
                logger.error(res.json())

            logger.debug("Uploading dashboard title")
            res = self.grimoire_con.post(url, data=json.dumps(data),
                                         headers=ES6_HEADER)
            try:
                res.raise_for_status()
            except requests.exceptions.HTTPError:
                logger.error("Couldn't create dashboard title.")
                logger.error(res.json())