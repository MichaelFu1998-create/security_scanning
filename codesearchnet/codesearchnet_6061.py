def handle_delete(self):
        """Change semantic of DELETE to remove resource tags."""
        # DELETE is only supported for the '/by_tag/' collection
        if "/by_tag/" not in self.path:
            raise DAVError(HTTP_FORBIDDEN)
        # path must be '/by_tag/<tag>/<resname>'
        catType, tag, _rest = util.save_split(self.path.strip("/"), "/", 2)
        assert catType == "by_tag"
        assert tag in self.data["tags"]
        self.data["tags"].remove(tag)
        return True