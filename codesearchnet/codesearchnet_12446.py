def remove_entity(self, name):
        """Unload an entity"""
        self.entities.remove(name)
        self.padaos.remove_entity(name)