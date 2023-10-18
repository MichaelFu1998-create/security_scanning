def submit_registration_form(self, form):
        """Submit a registration form.

        [client only]

        :Parameters:
            - `form`: the filled-in form. When form is `None` or its type is
              "cancel" the registration is to be canceled.

        :Types:
            - `form`: `pyxmpp.jabber.dataforms.Form`"""
        self.lock.acquire()
        try:
            if form and form.type!="cancel":
                self.registration_form = form
                iq = Iq(stanza_type = "set")
                iq.set_content(self.__register.submit_form(form))
                self.set_response_handlers(iq, self.registration_success, self.registration_error)
                self.send(iq)
            else:
                self.__register = None
        finally:
            self.lock.release()