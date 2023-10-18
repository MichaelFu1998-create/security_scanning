def p_typeDeclarationRHS(self, p):
        """typeDeclarationRHS : Syntax
                              | TEXTUAL_CONVENTION DisplayPart STATUS Status DESCRIPTION Text ReferPart SYNTAX Syntax
                              | choiceClause"""
        if p[1]:
            if p[1] == 'TEXTUAL-CONVENTION':
                p[0] = ('typeDeclarationRHS', p[2],  # display
                        p[4],  # status
                        (p[5], p[6]),  # description
                        p[7],  # reference
                        p[9])  # syntax
            else:
                p[0] = ('typeDeclarationRHS', p[1])