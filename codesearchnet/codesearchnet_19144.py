def from_whypo(cls, xml, encoding='utf-8'):
        """Constructor from xml element *WHYPO*

        :param xml.etree.ElementTree xml: the xml *WHYPO* element
        :param string encoding: encoding of the xml

        """
        word = unicode(xml.get('WORD'), encoding)
        confidence = float(xml.get('CM'))
        return cls(word, confidence)