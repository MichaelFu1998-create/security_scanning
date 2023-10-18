def __autorefresh_studies(self, cfg):
        """Execute autorefresh for areas of code study if configured"""

        if 'studies' not in self.conf[self.backend_section] or \
                'enrich_areas_of_code:git' not in self.conf[self.backend_section]['studies']:
            logger.debug("Not doing autorefresh for studies, Areas of Code study is not active.")
            return

        aoc_index = self.conf['enrich_areas_of_code:git'].get('out_index', GitEnrich.GIT_AOC_ENRICHED)

        # if `out_index` exists but has no value, use default
        if not aoc_index:
            aoc_index = GitEnrich.GIT_AOC_ENRICHED

        logger.debug("Autorefresh for Areas of Code study index: %s", aoc_index)

        es = Elasticsearch([self.conf['es_enrichment']['url']], timeout=100,
                           verify_certs=self._get_enrich_backend().elastic.requests.verify)

        if not es.indices.exists(index=aoc_index):
            logger.debug("Not doing autorefresh, index doesn't exist for Areas of Code study")
            return

        logger.debug("Doing autorefresh for Areas of Code study")

        # Create a GitEnrich backend tweaked to work with AOC index
        aoc_backend = GitEnrich(self.db_sh, None, cfg['projects']['projects_file'],
                                self.db_user, self.db_password, self.db_host)
        aoc_backend.mapping = None
        aoc_backend.roles = ['author']
        elastic_enrich = get_elastic(self.conf['es_enrichment']['url'],
                                     aoc_index, clean=False, backend=aoc_backend)
        aoc_backend.set_elastic(elastic_enrich)

        self.__autorefresh(aoc_backend, studies=True)