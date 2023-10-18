def from_shypo(cls, xml, encoding='utf-8'):
        """Constructor from xml element *SHYPO*

        :param xml.etree.ElementTree xml: the xml *SHYPO* element
        :param string encoding: encoding of the xml

        """
        score = float(xml.get('SCORE'))
        words = [Word.from_whypo(w_xml, encoding) for w_xml in xml.findall('WHYPO') if w_xml.get('WORD') not in ['<s>', '</s>']]
        return cls(words, score)