def get_password(self, service, username):
        """Get password of the username for the service
        """
        collection = self.get_preferred_collection()
        items = collection.search_items(
            {"username": username, "service": service})
        for item in items:
            if hasattr(item, 'unlock'):
                item.unlock()
            if item.is_locked():  # User dismissed the prompt
                raise KeyringLocked('Failed to unlock the item!')
            return item.get_secret().decode('utf-8')