def convert_li(self, markup):

        """ Subtitutes <li> content to Wikipedia markup.
        """
        
        for li in re.findall("<li;*?>", markup):
            markup = re.sub(li, "\n* ", markup)
        markup = markup.replace("</li>", "")
            
        return markup