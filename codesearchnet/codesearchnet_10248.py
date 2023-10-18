def get_images_bytesize_match(self, images):
        """\
        loop through all the images and find the ones
        that have the best bytez to even make them a candidate
        """
        cnt = 0
        max_bytes_size = 15728640
        good_images = []
        for image in images:
            if cnt > 30:
                return good_images
            src = self.parser.getAttribute(image, attr='src')
            src = self.build_image_path(src)
            src = self.add_schema_if_none(src)
            local_image = self.get_local_image(src)
            if local_image:
                filesize = local_image.bytes
                if (filesize == 0 or filesize > self.images_min_bytes) and filesize < max_bytes_size:
                    good_images.append(image)
                else:
                    images.remove(image)
            cnt += 1
        return good_images if len(good_images) > 0 else None