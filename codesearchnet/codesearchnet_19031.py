def get_queryset(self, request):
        """
        Add number of photos to each gallery.
        """
        qs = super(GalleryAdmin, self).get_queryset(request)
        return qs.annotate(photo_count=Count('photos'))