def __get_dash_menu(self, kibiter_major):
        """Order the dashboard menu"""

        # omenu = OrderedDict()
        omenu = []
        # Start with Overview
        omenu.append(self.menu_panels_common['Overview'])

        # Now the data _getsources
        ds_menu = self.__get_menu_entries(kibiter_major)

        # Remove the kafka and community menus, they will be included at the end
        kafka_menu = None
        community_menu = None

        found_kafka = [pos for pos, menu in enumerate(ds_menu) if menu['name'] == KAFKA_NAME]
        if found_kafka:
            kafka_menu = ds_menu.pop(found_kafka[0])

        found_community = [pos for pos, menu in enumerate(ds_menu) if menu['name'] == COMMUNITY_NAME]
        if found_community:
            community_menu = ds_menu.pop(found_community[0])

        ds_menu.sort(key=operator.itemgetter('name'))
        omenu += ds_menu

        # If kafka and community are present add them before the Data Status and About
        if kafka_menu:
            omenu.append(kafka_menu)

        if community_menu:
            omenu.append(community_menu)

        # At the end Data Status, About
        omenu.append(self.menu_panels_common['Data Status'])
        omenu.append(self.menu_panels_common['About'])

        logger.debug("Menu for panels: %s", json.dumps(ds_menu, indent=4))
        return omenu