def start_tag(self):
        '''Returns the elements HTML start tag'''
        direct_attributes = (attribute.render(self) for attribute in self.render_attributes)
        attributes = ()
        if hasattr(self, '_attributes'):
            attributes = ('{0}="{1}"'.format(key, value)
                                             for key, value in self.attributes.items() if value)

        rendered_attributes = " ".join(filter(bool, chain(direct_attributes, attributes)))
        return '<{0}{1}{2}{3}>'.format(self.tag, ' ' if rendered_attributes else '',
                                       rendered_attributes, ' /' if self.tag_self_closes else "")