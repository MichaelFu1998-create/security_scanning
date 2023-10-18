def parse_data(self, text, maxwidth, maxheight, template_dir, context, 
                   urlize_all_links):
        """
        Parses a block of text rendering links that occur on their own line
        normally but rendering inline links using a special template dir
        """
        block_parser = TextBlockParser()
        
        lines = text.splitlines()
        parsed = []
        
        for line in lines:
            if STANDALONE_URL_RE.match(line):
                user_url = line.strip()
                try:
                    resource = oembed.site.embed(user_url, maxwidth=maxwidth, maxheight=maxheight)
                    context['minwidth'] = min(maxwidth, resource.width)
                    context['minheight'] = min(maxheight, resource.height)
                except OEmbedException:
                    if urlize_all_links:
                        line = '<a href="%(LINK)s">%(LINK)s</a>' % {'LINK': user_url}
                else:
                    context['minwidth'] = min(maxwidth, resource.width)
                    context['minheight'] = min(maxheight, resource.height)
                    
                    line = self.render_oembed(
                        resource, 
                        user_url, 
                        template_dir=template_dir, 
                        context=context)
            else:
                line = block_parser.parse(line, maxwidth, maxheight, 'inline',
                                          context, urlize_all_links)
            
            parsed.append(line)
        
        return mark_safe('\n'.join(parsed))