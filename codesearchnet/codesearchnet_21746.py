def list_from_document(cls, doc):
        """Returns a list of TMDDEventConverter elements.

        doc is an XML Element containing one or more <FEU> events
        """
        objs = []
        for feu in doc.xpath('//FEU'):
            detail_els = feu.xpath('event-element-details/event-element-detail')
            for idx, detail in enumerate(detail_els):
                objs.append(cls(feu, detail, id_suffix=idx, number_in_group=len(detail_els)))
        return objs