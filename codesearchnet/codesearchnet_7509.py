def p_notificationGroupClause(self, p):
        """notificationGroupClause : LOWERCASE_IDENTIFIER NOTIFICATION_GROUP NotificationsPart STATUS Status DESCRIPTION Text ReferPart COLON_COLON_EQUAL '{' objectIdentifier '}'"""
        p[0] = ('notificationGroupClause',
                p[1],  # id
                p[3],  # notifications
                p[5],  # status
                (p[6], p[7]),  # description
                p[8],  # reference
                p[11])