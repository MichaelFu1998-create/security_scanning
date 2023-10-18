def p_objectitem_0(self, p):
        '''
        objectitem : objectkey EQUAL number
                   | objectkey EQUAL BOOL
                   | objectkey EQUAL STRING
                   | objectkey EQUAL object
                   | objectkey EQUAL list
        '''
        if DEBUG:
            self.print_p(p)
        p[0] = (p[1], p[3])