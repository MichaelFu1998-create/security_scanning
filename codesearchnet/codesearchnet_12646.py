def get_context_data(self, **kwargs):
        """Injects data into the context to replicate CBV ListView."""
        context = super(DocumentListView, self).get_context_data(**kwargs)
        context = self.set_permissions_in_context(context)

        if not context['has_view_permission']:
            return HttpResponseForbidden("You do not have permissions to view this content.")

        context['object_list'] = self.get_queryset()

        context['document'] = self.document
        context['app_label'] = self.app_label
        context['document_name'] = self.document_name
        context['request'] = self.request

        # pagination bits
        context['page'] = self.page
        context['documents_per_page'] = self.documents_per_page

        if self.page > 1:
            previous_page_number = self.page - 1
        else:
            previous_page_number = None

        if self.page < self.total_pages:
            next_page_number = self.page + 1
        else:
            next_page_number = None

        context['previous_page_number'] = previous_page_number
        context['has_previous_page'] = previous_page_number is not None
        context['next_page_number'] = next_page_number
        context['has_next_page'] = next_page_number is not None
        context['total_pages'] = self.total_pages

        # Part of upcoming list view form functionality
        if self.queryset.count():
            context['keys'] = ['id', ]

            # Show those items for which we've got list_fields on the mongoadmin
            for key in [x for x in self.mongoadmin.list_fields if x != 'id' and x in self.document._fields.keys()]:

                # TODO - Figure out why this EmbeddedDocumentField and ListField breaks this view
                # Note - This is the challenge part, right? :)
                if isinstance(self.document._fields[key], EmbeddedDocumentField):
                    continue
                if isinstance(self.document._fields[key], ListField):
                    continue
                context['keys'].append(key)

        if self.mongoadmin.search_fields:
            context['search_field'] = True

        return context