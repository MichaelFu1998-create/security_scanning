def load_entity(self, name, file_name, reload_cache=False):
        """
       Loads an entity, optionally checking the cache first

       Args:
           name (str): The associated name of the entity
           file_name (str): The location of the entity file
           reload_cache (bool): Whether to refresh all of cache
       """
        Entity.verify_name(name)
        self.entities.load(Entity.wrap_name(name), file_name, reload_cache)
        with open(file_name) as f:
            self.padaos.add_entity(name, f.read().split('\n'))
        self.must_train = True