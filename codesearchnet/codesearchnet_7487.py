def p_moduleIdentityClause(self, p):
        """moduleIdentityClause : LOWERCASE_IDENTIFIER MODULE_IDENTITY SubjectCategoriesPart LAST_UPDATED ExtUTCTime ORGANIZATION Text CONTACT_INFO Text DESCRIPTION Text RevisionPart COLON_COLON_EQUAL '{' objectIdentifier '}'"""
        p[0] = ('moduleIdentityClause', p[1],  # id
                #  p[2], # MODULE_IDENTITY
                # XXX  p[3], # SubjectCategoriesPart
                (p[4], p[5]),  # last updated
                (p[6], p[7]),  # organization
                (p[8], p[9]),  # contact info
                (p[10], p[11]),  # description
                p[12],  # RevisionPart
                p[15])