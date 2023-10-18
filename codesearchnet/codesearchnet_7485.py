def p_objectTypeClause(self, p):
        """objectTypeClause : LOWERCASE_IDENTIFIER OBJECT_TYPE SYNTAX Syntax UnitsPart MaxOrPIBAccessPart STATUS Status descriptionClause ReferPart IndexPart MibIndex DefValPart COLON_COLON_EQUAL '{' ObjectName '}'"""
        p[0] = ('objectTypeClause', p[1],  # id
                #  p[2], # OBJECT_TYPE
                p[4],  # syntax
                p[5],  # UnitsPart
                p[6],  # MaxOrPIBAccessPart
                p[8],  # status
                p[9],  # descriptionClause
                p[10],  # reference
                p[11],  # augmentions
                p[12],  # index
                p[13],  # DefValPart
                p[16])