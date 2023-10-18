def p_Notifications(self, p):
        """Notifications : Notifications ',' Notification
                         | Notification"""
        n = len(p)
        if n == 4:
            p[0] = ('Notifications', p[1][1] + [p[3]])
        elif n == 2:
            p[0] = ('Notifications', [p[1]])