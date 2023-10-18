def parse_theme(self, xml):
        
        """ Parses a theme from XML returned by Kuler.
        
        Gets the theme's id, label and swatches.
        All of the swatches are converted to RGB.
        If we have a full description for a theme id in cache,
        parse that to get tags associated with the theme.
        
        """

        kt = KulerTheme()        
        kt.author = xml.getElementsByTagName("author")[0]
        kt.author = kt.author.childNodes[1].childNodes[0].nodeValue
        kt.id = int(self.parse_tag(xml, "id"))
        kt.label = self.parse_tag(xml, "label")
        mode = self.parse_tag(xml, "mode")
        
        for swatch in xml.getElementsByTagName("swatch"):
            
            c1 = float(self.parse_tag(swatch, "c1"))
            c2 = float(self.parse_tag(swatch, "c2"))
            c3 = float(self.parse_tag(swatch, "c3"))
            c4 = float(self.parse_tag(swatch, "c4"))
            
            if mode == "rgb":
                kt.append((c1,c2,c3))
            if mode == "cmyk":   
                kt.append(cmyk_to_rgb(c1,c2,c3,c4))
            if mode == "hsv":
                kt.append(colorsys.hsv_to_rgb(c1,c2,c3))
            if mode == "hex":
                kt.append(hex_to_rgb(c1))
            if mode == "lab":
                kt.append(lab_to_rgb(c1,c2,c3))
        
        # If we have the full theme in cache,
        # parse tags from it.
        if self._cache.exists(self.id_string + str(kt.id)):
            xml = self._cache.read(self.id_string + str(kt.id))
            xml = minidom.parseString(xml)
        for tags in xml.getElementsByTagName("tag"):
            tags = self.parse_tag(tags, "label")
            tags = tags.split(" ")
            kt.tags.extend(tags)
        
        return kt