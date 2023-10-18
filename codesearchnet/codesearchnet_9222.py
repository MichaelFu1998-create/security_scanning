def __create_dashboard_menu(self, dash_menu, kibiter_major):
        """Create the menu definition to access the panels in a dashboard.

        :param          menu: dashboard menu to upload
        :param kibiter_major: major version of kibiter
        """
        logger.info("Adding dashboard menu")
        if kibiter_major == "6":
            menu_resource = ".kibana/doc/metadashboard"
            mapping_resource = ".kibana/_mapping/doc"
            mapping = {"dynamic": "true"}
            menu = {'metadashboard': dash_menu}
        else:
            menu_resource = ".kibana/metadashboard/main"
            mapping_resource = ".kibana/_mapping/metadashboard"
            mapping = {"dynamic": "true"}
            menu = dash_menu
        menu_url = urijoin(self.conf['es_enrichment']['url'],
                           menu_resource)

        mapping_url = urijoin(self.conf['es_enrichment']['url'],
                              mapping_resource)
        logger.debug("Adding mapping for metadashboard")
        res = self.grimoire_con.put(mapping_url, data=json.dumps(mapping),
                                    headers=ES6_HEADER)
        try:
            res.raise_for_status()
        except requests.exceptions.HTTPError:
            logger.error("Couldn't create mapping for Kibiter menu.")
        res = self.grimoire_con.post(menu_url, data=json.dumps(menu),
                                     headers=ES6_HEADER)
        try:
            res.raise_for_status()
        except requests.exceptions.HTTPError:
            logger.error("Couldn't create Kibiter menu.")
            logger.error(res.json())
            raise