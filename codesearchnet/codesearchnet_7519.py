def p_notificationTypeClause(self, p):
        """notificationTypeClause : fuzzy_lowercase_identifier NOTIFICATION_TYPE NotificationObjectsPart STATUS Status DESCRIPTION Text ReferPart COLON_COLON_EQUAL '{' NotificationName '}'"""  # some MIBs have uppercase and/or lowercase id
        p[0] = ('notificationTypeClause', p[1],  # id
                #  p[2], # NOTIFICATION_TYPE
                p[3],  # NotificationObjectsPart
                p[5],  # status
                (p[6], p[7]),  # description
                p[8],   # Reference
                p[11])