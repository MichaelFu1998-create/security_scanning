def parse_data(self, text, maxwidth, maxheight, template_dir, context,
                   urlize_all_links):
        """
        Parses a block of text indiscriminately
        """
        # create a dictionary of user urls -> rendered responses
        replacements = {}
        user_urls = set(re.findall(URL_RE, text))
        
        for user_url in user_urls:
            try:
                resource = oembed.site.embed(user_url, maxwidth=maxwidth, maxheight=maxheight)
            except OEmbedException:
                if urlize_all_links:
                    replacements[user_url] = '<a href="%(LINK)s">%(LINK)s</a>' % {'LINK': user_url}
            else:
                context['minwidth'] = min(maxwidth, resource.width)
                context['minheight'] = min(maxheight, resource.height)
                
                replacement = self.render_oembed(
                    resource, 
                    user_url, 
                    template_dir=template_dir, 
                    context=context
                )
                replacements[user_url] = replacement.strip()
        
        # go through the text recording URLs that can be replaced
        # taking note of their start & end indexes
        user_urls = re.finditer(URL_RE, text)
        matches = []
        for match in user_urls:
            if match.group() in replacements:
                matches.append([match.start(), match.end(), match.group()])
        
        # replace the URLs in order, offsetting the indices each go
        for indx, (start, end, user_url) in enumerate(matches):
            replacement = replacements[user_url]
            difference = len(replacement) - len(user_url)
            
            # insert the replacement between two slices of text surrounding the
            # original url
            text = text[:start] + replacement + text[end:]
            
            # iterate through the rest of the matches offsetting their indices
            # based on the difference between replacement/original
            for j in xrange(indx + 1, len(matches)):
                matches[j][0] += difference
                matches[j][1] += difference
        return mark_safe(text)