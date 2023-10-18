def formfield(self, **kwargs):
        """Get the form for field."""
        defaults = {
            'form_class': RichTextFormField,
            'config': self.config,
        }
        defaults.update(kwargs)
        return super(RichTextField, self).formfield(**defaults)