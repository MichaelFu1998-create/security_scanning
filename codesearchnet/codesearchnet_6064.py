def get_property_names(self, is_allprop):
        """Return list of supported property names in Clark Notation.

        See DAVResource.get_property_names()
        """
        # Let base class implementation add supported live and dead properties
        propNameList = super(VirtualResource, self).get_property_names(is_allprop)
        # Add custom live properties (report on 'allprop' and 'propnames')
        propNameList.extend(VirtualResource._supportedProps)
        return propNameList