def map_to_dictionary(self, url, obj, **kwargs):
        """
        Build a dictionary of metadata for the requested object.
        """
        maxwidth = kwargs.get('maxwidth', None)
        maxheight = kwargs.get('maxheight', None)
        
        provider_url, provider_name = self.provider_from_url(url)
        
        mapping = {
            'version': '1.0',
            'url': url,
            'provider_name': provider_name,
            'provider_url': provider_url,
            'type': self.resource_type
        }
        
        # a hook
        self.preprocess(obj, mapping, **kwargs)
        
        # resize image if we have a photo, otherwise use the given maximums
        if self.resource_type == 'photo' and self.get_image(obj):
            self.resize_photo(obj, mapping, maxwidth, maxheight)
        elif self.resource_type in ('video', 'rich', 'photo'):
            width, height = size_to_nearest(
                maxwidth,
                maxheight,
                self._meta.valid_sizes,
                self._meta.force_fit
            )
            mapping.update(width=width, height=height)
        
        # create a thumbnail
        if self.get_image(obj):
            self.thumbnail(obj, mapping)
        
        # map attributes to the mapping dictionary.  if the attribute is
        # a callable, it must have an argument signature of
        # (self, obj)
        for attr in ('title', 'author_name', 'author_url', 'html'):
            self.map_attr(mapping, attr, obj)
        
        # fix any urls
        if 'url' in mapping:
            mapping['url'] = relative_to_full(mapping['url'], url)
        
        if 'thumbnail_url' in mapping:
            mapping['thumbnail_url'] = relative_to_full(mapping['thumbnail_url'], url)
        
        if 'html' not in mapping and mapping['type'] in ('video', 'rich'):
            mapping['html'] = self.render_html(obj, context=Context(mapping))
        
        # a hook
        self.postprocess(obj, mapping, **kwargs)
        
        return mapping