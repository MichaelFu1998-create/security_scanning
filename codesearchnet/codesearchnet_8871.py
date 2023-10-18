def get_map_image(url, dest_path=None):
        """
        Return a requested map from a robot.

        :return:
        """
        image = requests.get(url, stream=True, timeout=10)

        if dest_path:
            image_url = url.rsplit('/', 2)[1] + '-' + url.rsplit('/', 1)[1]
            image_filename = image_url.split('?')[0]
            dest = os.path.join(dest_path, image_filename)
            image.raise_for_status()
            with open(dest, 'wb') as data:
                image.raw.decode_content = True
                shutil.copyfileobj(image.raw, data)

        return image.raw