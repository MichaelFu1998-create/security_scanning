def __get_menu_entries(self, kibiter_major):
        """ Get the menu entries from the panel definition """
        menu_entries = []
        for entry in self.panels_menu:
            if entry['source'] not in self.data_sources:
                continue
            parent_menu_item = {
                'name': entry['name'],
                'title': entry['name'],
                'description': "",
                'type': "menu",
                'dashboards': []
            }
            for subentry in entry['menu']:
                try:
                    dash_name = get_dashboard_name(subentry['panel'])
                except FileNotFoundError:
                    logging.error("Can't open dashboard file %s", subentry['panel'])
                    continue
                # The name for the entry is in self.panels_menu
                child_item = {
                    "name": subentry['name'],
                    "title": subentry['name'],
                    "description": "",
                    "type": "entry",
                    "panel_id": dash_name
                }
                parent_menu_item['dashboards'].append(child_item)
            menu_entries.append(parent_menu_item)

        return menu_entries