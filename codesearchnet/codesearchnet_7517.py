def p_typeSMIv1(self, p):
        """typeSMIv1 : INTEGER
                     | OCTET STRING
                     | IPADDRESS
                     | NETWORKADDRESS"""
        n = len(p)
        indextype = n == 3 and p[1] + ' ' + p[2] or p[1]
        p[0] = indextype