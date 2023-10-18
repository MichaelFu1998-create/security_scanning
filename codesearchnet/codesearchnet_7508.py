def p_objectGroupClause(self, p):
        """objectGroupClause : LOWERCASE_IDENTIFIER OBJECT_GROUP ObjectGroupObjectsPart STATUS Status DESCRIPTION Text ReferPart COLON_COLON_EQUAL '{' objectIdentifier '}'"""
        p[0] = ('objectGroupClause',
                p[1],  # id
                p[3],  # objects
                p[5],  # status
                (p[6], p[7]),  # description
                p[8],  # reference
                p[11])