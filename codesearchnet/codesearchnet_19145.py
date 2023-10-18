def run(self):
        """Start listening to the server"""
        logger.info(u'Started listening')
        while not self._stop:
            xml = self._readxml()

            # Exit on invalid XML
            if xml is None:
                break

            # Raw xml only
            if not self.modelize:
                logger.info(u'Raw xml: %s' % xml)
                self.results.put(xml)
                continue

            # Model objects + raw xml as fallback
            if xml.tag == 'RECOGOUT':
                sentence = Sentence.from_shypo(xml.find('SHYPO'), self.encoding)
                logger.info(u'Modelized recognition: %r' % sentence)
                self.results.put(sentence)
            else:
                logger.info(u'Unmodelized xml: %s' % xml)
                self.results.put(xml)

        logger.info(u'Stopped listening')