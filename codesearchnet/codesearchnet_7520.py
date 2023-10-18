def p_trapTypeClause(self, p):
        """trapTypeClause : fuzzy_lowercase_identifier TRAP_TYPE EnterprisePart VarPart DescrPart ReferPart COLON_COLON_EQUAL NUMBER"""
        # libsmi: TODO: range of number?
        p[0] = ('trapTypeClause', p[1],  # fuzzy_lowercase_identifier
                #  p[2], # TRAP_TYPE
                p[3],  # EnterprisePart (objectIdentifier)
                p[4],  # VarPart
                p[5],  # description
                p[6],  # reference
                p[8])