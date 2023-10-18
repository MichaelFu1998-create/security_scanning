def handle_copy(self, dest_path, depth_infinity):
        """Change semantic of COPY to add resource tags."""
        # destPath must be '/by_tag/<tag>/<resname>'
        if "/by_tag/" not in dest_path:
            raise DAVError(HTTP_FORBIDDEN)
        catType, tag, _rest = util.save_split(dest_path.strip("/"), "/", 2)
        assert catType == "by_tag"
        if tag not in self.data["tags"]:
            self.data["tags"].append(tag)
        return True