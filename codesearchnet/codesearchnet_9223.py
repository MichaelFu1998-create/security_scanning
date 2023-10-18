def __remove_dashboard_menu(self, kibiter_major):
        """Remove existing menu for dashboard, if any.

        Usually, we remove the menu before creating a new one.

        :param kibiter_major: major version of kibiter
        """
        logger.info("Removing old dashboard menu, if any")
        if kibiter_major == "6":
            metadashboard = ".kibana/doc/metadashboard"
        else:
            metadashboard = ".kibana/metadashboard/main"
        menu_url = urijoin(self.conf['es_enrichment']['url'], metadashboard)
        self.grimoire_con.delete(menu_url)