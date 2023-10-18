def get_images(self, private=False, type=None):
        """
            This function returns a list of Image object.
        """
        params = {}
        if private:
            params['private'] = 'true'
        if type:
            params['type'] = type
        data = self.get_data("images/", params=params)
        images = list()
        for jsoned in data['images']:
            image = Image(**jsoned)
            image.token = self.token
            images.append(image)
        return images