def p_moduleComplianceClause(self, p):
        """moduleComplianceClause : LOWERCASE_IDENTIFIER MODULE_COMPLIANCE STATUS Status DESCRIPTION Text ReferPart ComplianceModulePart COLON_COLON_EQUAL '{' objectIdentifier '}'"""
        p[0] = ('moduleComplianceClause',
                p[1],  # id
                #  p[2], # MODULE_COMPLIANCE
                p[4],  # status
                (p[5], p[6]),  # description
                p[7],  # reference
                p[8],  # ComplianceModules
                p[11])