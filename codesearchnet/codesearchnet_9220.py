def create_dashboard(self, panel_file, data_sources=None, strict=True):
        """Upload a panel to Elasticsearch if it does not exist yet.

        If a list of data sources is specified, upload only those
        elements (visualizations, searches) that match that data source.

        :param panel_file: file name of panel (dashobard) to upload
        :param data_sources: list of data sources
        :param strict: only upload a dashboard if it is newer than the one already existing
        """
        es_enrich = self.conf['es_enrichment']['url']
        kibana_url = self.conf['panels']['kibiter_url']

        mboxes_sources = set(['pipermail', 'hyperkitty', 'groupsio', 'nntp'])
        if data_sources and any(x in data_sources for x in mboxes_sources):
            data_sources = list(data_sources)
            data_sources.append('mbox')
        if data_sources and ('supybot' in data_sources):
            data_sources = list(data_sources)
            data_sources.append('irc')
        if data_sources and 'google_hits' in data_sources:
            data_sources = list(data_sources)
            data_sources.append('googlehits')
        if data_sources and 'stackexchange' in data_sources:
            # stackexchange is called stackoverflow in panels
            data_sources = list(data_sources)
            data_sources.append('stackoverflow')
        if data_sources and 'phabricator' in data_sources:
            data_sources = list(data_sources)
            data_sources.append('maniphest')

        try:
            import_dashboard(es_enrich, kibana_url, panel_file, data_sources=data_sources, strict=strict)
        except ValueError:
            logger.error("%s does not include release field. Not loading the panel.", panel_file)
        except RuntimeError:
            logger.error("Can not load the panel %s", panel_file)