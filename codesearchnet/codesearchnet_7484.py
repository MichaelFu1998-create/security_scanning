def p_objectIdentityClause(self, p):
        """objectIdentityClause : LOWERCASE_IDENTIFIER OBJECT_IDENTITY STATUS Status DESCRIPTION Text ReferPart COLON_COLON_EQUAL '{' objectIdentifier '}'"""
        p[0] = ('objectIdentityClause', p[1],  # id
                #  p[2], # OBJECT_IDENTITY
                p[4],  # status
                (p[5], p[6]),  # description
                p[7],  # reference
                p[10])