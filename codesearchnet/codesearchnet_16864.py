def create_email(self, name, subject, html, text=''):
        """ [DECPRECATED] API call to create an email """
        return self.create_template(name, subject, html, text)