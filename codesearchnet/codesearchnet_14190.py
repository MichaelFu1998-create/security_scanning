def parse_links(self, markup):
        
        """ Returns a list of internal Wikipedia links in the markup.

        # A Wikipedia link looks like:
        # [[List of operating systems#Embedded | List of embedded operating systems]]
        # It does not contain a colon, this indicates images, users, languages, etc.
        
        The return value is a list containing the first part of the link,
        without the anchor.

        """
        
        links = []
        m = re.findall(self.re["link"], markup)
        for link in m:
            # We don't like [[{{{1|Universe (disambiguation)}}}]]
            if link.find("{") >= 0:
                link = re.sub("\{{1,3}[0-9]{0,2}\|", "", link)
                link = link.replace("{", "")
                link = link.replace("}", "")            
            link = link.split("|")
            link[0] = link[0].split("#")
            page = link[0][0].strip()
            #anchor = u""
            #display = u""
            #if len(link[0]) > 1: 
            #    anchor = link[0][1].strip()
            #if len(link) > 1: 
            #    display = link[1].strip()
            if not page in links:
                links.append(page)
                #links[page] = WikipediaLink(page, anchor, display)
        
        links.sort()
        return links