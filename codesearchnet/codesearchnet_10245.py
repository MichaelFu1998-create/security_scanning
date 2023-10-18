def check_large_images(self, node, parent_depth_level, sibling_depth_level):
        """\
        although slow the best way to determine the best image is to download
        them and check the actual dimensions of the image when on disk
        so we'll go through a phased approach...
        1. get a list of ALL images from the parent node
        2. filter out any bad image names that we know of (gifs, ads, etc..)
        3. do a head request on each file to make sure it meets
           our bare requirements
        4. any images left over let's do a full GET request,
           download em to disk and check their dimensions
        5. Score images based on different factors like height/width
           and possibly things like color density
        """
        good_images = self.get_image_candidates(node)

        if good_images:
            scored_images = self.fetch_images(good_images, parent_depth_level)
            if scored_images:
                highscore_image = sorted(list(scored_images.items()),
                                         key=lambda x: x[1], reverse=True)[0][0]
                main_image = Image()
                main_image._src = highscore_image.src
                main_image._width = highscore_image.width
                main_image._height = highscore_image.height
                main_image._extraction_type = "bigimage"
                score_len = len(scored_images)
                main_image._confidence_score = 100 / score_len if score_len > 0 else 0
                return main_image

        depth_obj = self.get_depth_level(node, parent_depth_level, sibling_depth_level)
        if depth_obj:
            return self.check_large_images(depth_obj.node, depth_obj.parent_depth,
                                           depth_obj.sibling_depth)

        return None