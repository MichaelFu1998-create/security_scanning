def is_highlink_density(self, element):
        """
        checks the density of links within a node,
        is there not much text and most of it contains linky shit?
        if so it's no good
        """
        links = self.parser.getElementsByTag(element, tag='a')
        if not links:
            return False

        text = self.parser.getText(element)
        words = text.split(' ')
        words_number = float(len(words))
        link_text_parts = []
        for link in links:
            link_text_parts.append(self.parser.getText(link))

        link_text = ''.join(link_text_parts)
        link_words = link_text.split(' ')
        number_of_link_words = float(len(link_words))
        number_of_links = float(len(links))
        link_divisor = float(number_of_link_words / words_number)
        score = float(link_divisor * number_of_links)
        if score >= 1.0:
            return True
        return False