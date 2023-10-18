def add_entity(self, name, lines, reload_cache=False):
        """
        Adds an entity that matches the given lines.

        Example:
            self.add_intent('weather', ['will it rain on {weekday}?'])
            self.add_entity('{weekday}', ['monday', 'tuesday', 'wednesday'])  # ...

        Args:
            name (str): The name of the entity
            lines (list<str>): Lines of example extracted entities
            reload_cache (bool): Whether to refresh all of cache
        """
        Entity.verify_name(name)
        self.entities.add(Entity.wrap_name(name), lines, reload_cache)
        self.padaos.add_entity(name, lines)
        self.must_train = True