def handle_move(self, dest_path):
        """Change semantic of MOVE to change resource tags."""
        # path and destPath must be '/by_tag/<tag>/<resname>'
        if "/by_tag/" not in self.path:
            raise DAVError(HTTP_FORBIDDEN)
        if "/by_tag/" not in dest_path:
            raise DAVError(HTTP_FORBIDDEN)
        catType, tag, _rest = util.save_split(self.path.strip("/"), "/", 2)
        assert catType == "by_tag"
        assert tag in self.data["tags"]
        self.data["tags"].remove(tag)
        catType, tag, _rest = util.save_split(dest_path.strip("/"), "/", 2)
        assert catType == "by_tag"
        if tag not in self.data["tags"]:
            self.data["tags"].append(tag)
        return True