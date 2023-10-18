def get_queryset(self):
        """Replicates Django CBV `get_queryset()` method, but for MongoEngine.
        """
        if hasattr(self, "queryset") and self.queryset:
            return self.queryset

        self.set_mongonaut_base()
        self.set_mongoadmin()
        self.document = getattr(self.models, self.document_name)
        queryset = self.document.objects.all()

        if self.mongoadmin.ordering:
            queryset = queryset.order_by(*self.mongoadmin.ordering)

        # search. move this to get_queryset
        # search. move this to get_queryset
        q = self.request.GET.get('q')
        queryset = self.get_qset(queryset, q)

        ### Start pagination
        ### Note:
        ###    Can't use Paginator in Django because mongoengine querysets are
        ###    not the same as Django ORM querysets and it broke.
        # Make sure page request is an int. If not, deliver first page.
        try:
            self.page = int(self.request.GET.get('page', '1'))
        except ValueError:
            self.page = 1

        obj_count = queryset.count()
        self.total_pages = math.ceil(obj_count / self.documents_per_page)

        if self.page > self.total_pages:
            self.page = self.total_pages

        if self.page < 1:
            self.page = 1

        start = (self.page - 1) * self.documents_per_page
        end = self.page * self.documents_per_page

        queryset = queryset[start:end] if obj_count else queryset
        self.queryset = queryset
        return queryset