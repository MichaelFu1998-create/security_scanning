def parse_gallery_images(self, markup):
        
        """ Parses images from the <gallery></gallery> section.
        
        Images inside <gallery> tags do not have outer "[[" brackets.
        Add these and then parse again.
        
        """
        
        gallery = re.search(self.re["gallery"], markup)
        if gallery:
            gallery = gallery.group(1)
            gallery = gallery.replace("Image:", "[[Image:")
            gallery = gallery.replace("\n", "]]\n")
            images, markup = self.parse_images(gallery)
            return images
        
        return []