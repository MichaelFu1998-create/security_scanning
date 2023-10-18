def parse(self, text, maxwidth=None, maxheight=None, template_dir=None,
              context=None, urlize_all_links=CONSUMER_URLIZE_ALL):
        """
        Scans a block of text, replacing anything matching a provider pattern
        with an OEmbed html snippet, if possible.
        
        Templates should be stored at oembed/{format}.html, so for example:
            
            oembed/video.html
        
        An optional template_dir can be provided, allowing for
        
            oembed/[template_dir]/video.html
            
        These templates are passed a context variable, ``response``, which is
        an OEmbedResource, as well as the ``original_url``
        """
        context = context or Context()
        context['maxwidth'] = maxwidth
        context['maxheight'] = maxheight

        try:
            text = unicode(text)
        except UnicodeDecodeError:
            text = unicode(text.decode('utf-8'))
        
        return self.parse_data(text, maxwidth, maxheight, template_dir,
                               context, urlize_all_links)