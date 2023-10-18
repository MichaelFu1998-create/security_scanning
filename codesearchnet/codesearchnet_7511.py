def p_ComplianceModules(self, p):
        """ComplianceModules : ComplianceModules ComplianceModule
                             | ComplianceModule"""
        n = len(p)
        if n == 3:
            p[0] = ('ComplianceModules', p[1][1] + [p[2]])
        elif n == 2:
            p[0] = ('ComplianceModules', [p[1]])