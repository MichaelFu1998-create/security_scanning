def p_ComplianceModule(self, p):
        """ComplianceModule : MODULE ComplianceModuleName MandatoryPart CompliancePart"""
        objects = p[3] and p[3][1] or []
        objects += p[4] and p[4][1] or []
        p[0] = (p[2],  # ModuleName
                objects)