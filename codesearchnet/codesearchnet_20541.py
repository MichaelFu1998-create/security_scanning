def check_compatibility(self, one_img, another_img=None):
        """
        Parameters
        ----------
        one_img: str or img-like object.
            See NeuroImage constructor docstring.

        anoter_img: str or img-like object.
            See NeuroImage constructor docstring.
            If None will use the first image of self.images, if there is any.

        Raises
        ------
        NiftiFilesNotCompatible
            If one_img and another_img aren't compatible.

        ValueError
            If another_img is None and there are no other images in this set.
        """
        if another_img is None:
            if len(self.items) > 0:
                another_img = self.items[0]
            else:
                raise ValueError('self.items is empty, need an image to compare '
                                 'with {}'.format(repr_imgs(one_img)))

        try:
            if self.all_compatible:
                check_img_compatibility(one_img, another_img)
            if self.mask is not None:
                check_img_compatibility(one_img, self.mask, only_check_3d=True)
        except:
            raise