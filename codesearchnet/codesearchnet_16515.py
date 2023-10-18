def __general(self):
        """Level-0 parser and main loop.

        Look for a token that matches a level-1 parser and hand over control."""
        while 1:                            # main loop
            try:
                tok = self.__peek()         # only peek, apply_parser() will consume
            except DXParserNoTokens:
                # save previous DXInitObject
                # (kludge in here as the last level-2 parser usually does not return
                # via the object parser)
                if self.currentobject and self.currentobject not in self.objects:
                    self.objects.append(self.currentobject)
                return                      # stop parsing and finish
            # decision branches for all level-1 parsers:
            # (the only way to get out of the lower level parsers!)
            if tok.iscode('COMMENT'):
                self.set_parser('comment')  # switch the state
            elif tok.iscode('WORD') and tok.equals('object'):
                self.set_parser('object')   # switch the state
            elif self.__parser is self.__general:
                # Either a level-2 parser screwed up or some level-1
                # construct is not implemented.  (Note: this elif can
                # be only reached at the beginning or after comments;
                # later we never formally switch back to __general
                # (would create inifinite loop)
                raise DXParseError('Unknown level-1 construct at '+str(tok))

            self.apply_parser()