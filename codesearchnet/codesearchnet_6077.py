def get_property_names(self, is_allprop):
        """Return list of supported property names in Clark Notation.

        See DAVResource.get_property_names()
        """
        # Let base class implementation add supported live and dead properties
        propNameList = super(HgResource, self).get_property_names(is_allprop)
        # Add custom live properties (report on 'allprop' and 'propnames')
        if self.fctx:
            propNameList.extend(
                [
                    "{hg:}branch",
                    "{hg:}date",
                    "{hg:}description",
                    "{hg:}filerev",
                    "{hg:}rev",
                    "{hg:}user",
                ]
            )
        return propNameList