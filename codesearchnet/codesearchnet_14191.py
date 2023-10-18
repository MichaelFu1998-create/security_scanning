def parse_images(self, markup, treshold=6):
        
        """ Returns a list of images found in the markup.
        
        An image has a pathname, a description in plain text
        and a list of properties Wikipedia uses to size and place images.

        # A Wikipedia image looks like:
        # [[Image:Columbia Supercomputer - NASA Advanced Supercomputing Facility.jpg|right|thumb|
        #   The [[NASA]] [[Columbia (supercomputer)|Columbia Supercomputer]].]]
        # Parts are separated by "|".
        # The first part is the image file, the last part can be a description.
        # In between are display properties, like "right" or "thumb".
        
        """
        
        images = []
        m = re.findall(self.re["image"], markup)
        for p in m:
            p = self.parse_balanced_image(p)
            img = p.split("|")
            path = img[0].replace("[[Image:", "").strip()
            description = u""
            links = {}
            properties = []
            if len(img) > 1:
                img = "|".join(img[1:])
                links = self.parse_links(img)
                properties = self.plain(img).split("|")
                description = u""
                # Best guess: an image description is normally
                # longer than six characters, properties like
                # "thumb" and "right" are less than six characters.
                if len(properties[-1]) > treshold:
                    description = properties[-1]
                    properties = properties[:-1]
            img = WikipediaImage(path, description, links, properties)
            images.append(img)
            markup = markup.replace(p, "")
        
        return images, markup.strip()