def get_context_data(self, **kwargs):
        """
        Adds tab information to context.

        To retrieve a list of all group tab instances, use
        ``{{ tabs }}`` in your template.

        The id of the current tab is added as ``current_tab_id`` to the
        template context.

        If the current tab has a parent tab the parent's id is added to
        the template context as ``parent_tab_id``. Instances of all tabs
        of the parent level are added as ``parent_tabs`` to the context.

        If the current tab has children they are added to the template
        context as ``child_tabs``.

        """
        context = super(TabView, self).get_context_data(**kwargs)

        # Update the context with kwargs, TemplateView doesn't do this.
        context.update(kwargs)

        # Add tabs and "current" references to context
        process_tabs_kwargs = {
            'tabs': self.get_group_tabs(),
            'current_tab': self,
            'group_current_tab': self,
        }
        context['tabs'] = self._process_tabs(**process_tabs_kwargs)
        context['current_tab_id'] = self.tab_id

        # Handle parent tabs
        if self.tab_parent is not None:
            # Verify that tab parent is valid
            if self.tab_parent not in self._registry:
                msg = '%s has no attribute _is_tab' % self.tab_parent.__class__.__name__
                raise ImproperlyConfigured(msg)

            # Get parent tab instance
            parent = self.tab_parent()

            # Add parent tabs to context
            process_parents_kwargs = {
                'tabs': parent.get_group_tabs(),
                'current_tab': self,
                'group_current_tab': parent,
            }
            context['parent_tabs'] = self._process_tabs(**process_parents_kwargs)
            context['parent_tab_id'] = parent.tab_id

        # Handle child tabs
        if self.tab_id in self._children:
            process_children_kwargs = {
                'tabs': [t() for t in self._children[self.tab_id]],
                'current_tab': self,
                'group_current_tab': None,
            }
            context['child_tabs'] = self._process_tabs(**process_children_kwargs)

        return context