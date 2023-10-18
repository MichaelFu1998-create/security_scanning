def get_all_images_count(self):
        """
        Gets count of all images from both event and updates.
        """
        self_imgs = self.image_set.count()
        update_ids = self.update_set.values_list('id', flat=True)
        u_images = UpdateImage.objects.filter(update__id__in=update_ids).count()
        count = self_imgs + u_images

        return count