def delete_password(self, service, username):
        """Delete the stored password (only the first one)
        """
        collection = self.get_preferred_collection()
        items = collection.search_items(
            {"username": username, "service": service})
        for item in items:
            return item.delete()
        raise PasswordDeleteError("No such password!")