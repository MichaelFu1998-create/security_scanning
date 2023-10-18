def post(self, request, *args, **kwargs):
        """Creates new mongoengine records."""
        # TODO - make sure to check the rights of the poster
        #self.get_queryset() # TODO - write something that grabs the document class better
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        mongo_ids = self.get_initial()['mongo_id']
        for form_mongo_id in form.data.getlist('mongo_id'):
            for mongo_id in mongo_ids:
                if form_mongo_id == mongo_id:
                    self.document.objects.get(pk=mongo_id).delete()

        return self.form_invalid(form)