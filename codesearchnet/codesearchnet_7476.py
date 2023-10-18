def p_importPart(self, p):
        """importPart : imports
                      | empty"""
        # libsmi: TODO: ``IMPORTS ;'' allowed? refer ASN.1!
        if p[1]:
            importDict = {}
            for imp in p[1]:  # don't do just dict() because moduleNames may be repeated
                fromModule, symbols = imp
                if fromModule in importDict:
                    importDict[fromModule] += symbols
                else:
                    importDict[fromModule] = symbols

            p[0] = importDict