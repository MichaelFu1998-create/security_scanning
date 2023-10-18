def find_in_app(self, app, path):
        """
        Find a requested media file in an app's media fixtures locations.
        """
        storage = self.storages.get(app, None)
        if storage:
            # only try to find a file if the source dir actually exists
            if storage.exists(path):
                matched_path = storage.path(path)
                if matched_path:
                    return matched_path