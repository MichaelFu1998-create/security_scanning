def get_blueprint_routes(app, base_path):
        """Returns detailed information about registered blueprint routes matching the `BlueprintBundle` path

        :param app: App instance to obtain rules from
        :param base_path: Base path to return detailed route info for
        :return: List of route detail dicts
        """

        routes = []

        for child in app.url_map.iter_rules():
            if child.rule.startswith(base_path):
                relative_path = child.rule[len(base_path):]
                routes.append({
                    'path': relative_path,
                    'endpoint': child.endpoint,
                    'methods': list(child.methods)
                })

        return routes