def request_resource(self, url, **kwargs):
        """
        Request an OEmbedResource for a given url.  Some valid keyword args:
        - format
        - maxwidth
        - maxheight
        """
        obj = self.get_object(url)
        
        mapping = self.map_to_dictionary(url, obj, **kwargs)
        
        resource = OEmbedResource.create(mapping)
        resource.content_object = obj
        
        return resource