def resize(self, image_field, new_width=None, new_height=None):
        """
        Resize an image to the 'best fit' width & height, maintaining
        the scale of the image, so a 500x500 image sized to 300x400
        will actually be scaled to 300x300.
        
        Params:
        image: ImageFieldFile to be resized (i.e. model.image_field)
        new_width & new_height: desired maximums for resizing
        
        Returns:
        the url to the new image and the new width & height
        (http://path-to-new-image, 300, 300)
        """
        if isinstance(image_field, ImageFieldFile) and \
           image_field.field.width_field and \
           image_field.field.height_field:
            # use model fields
            current_width = getattr(image_field.instance, image_field.field.width_field)
            current_height = getattr(image_field.instance, image_field.field.height_field)
        else:
            # use PIL
            try:
                file_obj = storage.default_storage.open(image_field.name, 'rb')
                img_obj = Image.open(file_obj)
                current_width, current_height = img_obj.size
            except IOError:
                return (image_field.url, 0, 0) 
        
        # determine if resizing needs to be done (will not scale up)
        if current_width < new_width:
            if not new_height or current_height < new_height:
                return (image_field.url, current_width, current_height)
        
        # calculate ratios
        new_width, new_height = scale(current_width, current_height, new_width, new_height)
        
        # use the image_processor defined in the settings, or PIL by default
        return self._meta.image_processor.resize(image_field, new_width, new_height)