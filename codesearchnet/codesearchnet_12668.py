def sendmail(self, msg_from, msg_to, msg):
        """Remember the recipients."""
        SMTP_dummy.msg_from = msg_from
        SMTP_dummy.msg_to = msg_to
        SMTP_dummy.msg = msg