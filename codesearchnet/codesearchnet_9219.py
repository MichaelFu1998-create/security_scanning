def __kibiter_version(self):
        """ Get the kibiter vesion.

        :param major: major Elasticsearch version
        """
        version = None

        es_url = self.conf['es_enrichment']['url']
        config_url = '.kibana/config/_search'
        url = urijoin(es_url, config_url)
        version = None
        try:
            res = self.grimoire_con.get(url)
            res.raise_for_status()
            version = res.json()['hits']['hits'][0]['_id']
            logger.debug("Kibiter version: %s", version)
        except requests.exceptions.HTTPError:
            logger.warning("Can not find Kibiter version")

        return version