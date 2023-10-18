def get_video(self, node):
        """
        Create a video object from a video embed
        """
        video = Video()
        video._embed_code = self.get_embed_code(node)
        video._embed_type = self.get_embed_type(node)
        video._width = self.get_width(node)
        video._height = self.get_height(node)
        video._src = self.get_src(node)
        video._provider = self.get_provider(video.src)
        return video