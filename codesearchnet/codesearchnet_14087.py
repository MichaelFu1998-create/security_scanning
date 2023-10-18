def image_to_rgb(self, path, n=10):
        """
        Returns a list of colors based on pixel values in the image.

        The Core Image library must be present to determine pixel colors.
        F. Albers: http://nodebox.net/code/index.php/shared_2007-06-11-11-37-05

        """
        from PIL import Image
        img = Image.open(path)
        p = img.getdata()
        f = lambda p: choice(p)

        for i in _range(n):
            rgba = f(p)
            rgba = _list(rgba)
            if len(rgba) == 3:
                rgba.append(255)
            r, g, b, a = [v / 255.0 for v in rgba]
            clr = color(r, g, b, a, mode="rgb")
            self.append(clr)