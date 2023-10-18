def get_all_images(self):
        """
        Returns chained list of event and update images.
        """
        self_imgs = self.image_set.all()
        update_ids = self.update_set.values_list('id', flat=True)
        u_images = UpdateImage.objects.filter(update__id__in=update_ids)

        return list(chain(self_imgs, u_images))