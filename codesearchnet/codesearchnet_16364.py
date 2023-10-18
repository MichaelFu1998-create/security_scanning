def value_from_datadict(self, *args, **kwargs):
        """
        Pass the submitted value through the sanitizer before returning it.
        """
        value = super(RichTextWidget, self).value_from_datadict(
            *args, **kwargs)
        if value is not None:
            value = self.get_sanitizer()(value)
        return value