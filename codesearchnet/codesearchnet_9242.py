def es_version(self, url):
        """Get Elasticsearch version.

        Get the version of Elasticsearch. This is useful because
        Elasticsearch and Kibiter are paired (same major version for 5, 6).

        :param url: Elasticseearch url hosting Kibiter indices
        :returns:   major version, as string
        """

        try:
            res = self.grimoire_con.get(url)
            res.raise_for_status()
            major = res.json()['version']['number'].split(".")[0]
        except Exception:
            logger.error("Error retrieving Elasticsearch version: " + url)
            raise
        return major