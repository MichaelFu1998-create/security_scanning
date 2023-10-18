def _load_images_and_labels(self, images, labels=None):
        """Read the images, load them into self.items and set the labels."""
        if not isinstance(images, (list, tuple)):
            raise ValueError('Expected an iterable (list or tuple) of strings or img-like objects. '
                             'Got a {}.'.format(type(images)))

        if not len(images) > 0:
            raise ValueError('Expected an iterable (list or tuple) of strings or img-like objects '
                             'of size higher than 0. Got {} items.'.format(len(images)))

        if labels is not None and len(labels) != len(images):
            raise ValueError('Expected the same length for image set ({}) and '
                             'labels list ({}).'.format(len(images), len(labels)))

        first_file = images[0]
        if first_file:
            first_img = NeuroImage(first_file)
        else:
            raise('Error reading image {}.'.format(repr_imgs(first_file)))

        for idx, image in enumerate(images):
            try:
                img = NeuroImage(image)
                self.check_compatibility(img, first_img)
            except:
                log.exception('Error reading image {}.'.format(repr_imgs(image)))
                raise
            else:
                self.items.append(img)

        self.set_labels(labels)