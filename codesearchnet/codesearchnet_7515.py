def p_agentCapabilitiesClause(self, p):
        """agentCapabilitiesClause : LOWERCASE_IDENTIFIER AGENT_CAPABILITIES PRODUCT_RELEASE Text STATUS Status DESCRIPTION Text ReferPart ModulePart_Capabilities COLON_COLON_EQUAL '{' objectIdentifier '}'"""
        p[0] = ('agentCapabilitiesClause', p[1],  # id
                #   p[2], # AGENT_CAPABILITIES
                (p[3], p[4]),  # product release
                p[6],  # status
                (p[7], p[8]),  # description
                p[9],  # reference
                #   p[10], # module capabilities
                p[13])