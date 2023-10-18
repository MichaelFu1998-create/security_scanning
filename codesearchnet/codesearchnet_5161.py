def get_global_images(self):
        """
            This function returns a list of Image objects representing
            public DigitalOcean images (e.g. base distribution images
            and 'One-Click' applications).
        """
        data = self.get_images()
        images = list()
        for i in data:
            if i.public:
                i.token = self.token
                images.append(i)
        return images