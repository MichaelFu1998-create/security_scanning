def process_post_form(self, success_message=None):
        """
        As long as the form is set on the view this method will validate the form
        and save the submitted data.  Only call this if you are posting data.
        The given success_message will be used with the djanog messages framework
        if the posted data sucessfully submits.
        """

        # When on initial args are given we need to set the base document.
        if not hasattr(self, 'document') or self.document is None:
            self.document = self.document_type()
        self.form = MongoModelForm(model=self.document_type, instance=self.document,
                                   form_post_data=self.request.POST).get_form()
        self.form.is_bound = True
        if self.form.is_valid():

            self.document_map_dict = MongoModelForm(model=self.document_type).create_document_dictionary(self.document_type)
            self.new_document = self.document_type

            # Used to keep track of embedded documents in lists.  Keyed by the list and the number of the
            # document.
            self.embedded_list_docs = {}

            if self.new_document is None:
                messages.error(self.request, u"Failed to save document")
            else:
                self.new_document = self.new_document()

                for form_key in self.form.cleaned_data.keys():
                    if form_key == 'id' and hasattr(self, 'document'):
                        self.new_document.id = self.document.id
                        continue
                    self.process_document(self.new_document, form_key, None)

                self.new_document.save()
                if success_message:
                    messages.success(self.request, success_message)

        return self.form