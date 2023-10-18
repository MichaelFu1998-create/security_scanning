def drawimage(self, image, x=None, y=None):
        """
        :param image: Image to draw
        :param x: optional, x coordinate (default is image.x)
        :param y: optional, y coordinate (default is image.y)
        :return:
        """
        if x is None:
            x = image.x
        if y is None:
            y = image.y
        self.image(image.path, image.x, image.y, data=image.data)