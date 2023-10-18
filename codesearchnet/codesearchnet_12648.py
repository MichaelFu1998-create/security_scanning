def get_context_data(self, **kwargs):
        """ TODO - possibly inherit this from DocumentEditFormView. This is same thing minus:
            self.ident = self.kwargs.get('id')
            self.document = self.document_type.objects.get(pk=self.ident)
        """
        context = super(DocumentAddFormView, self).get_context_data(**kwargs)
        self.set_mongoadmin()
        context = self.set_permissions_in_context(context)
        self.document_type = getattr(self.models, self.document_name)

        context['app_label'] = self.app_label
        context['document_name'] = self.document_name
        context['form_action'] = reverse('document_detail_add_form', args=[self.kwargs.get('app_label'),
                                                                           self.kwargs.get('document_name')])

        return context