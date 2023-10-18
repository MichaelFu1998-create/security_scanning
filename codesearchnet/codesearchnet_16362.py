def _create_formsets(self, request, obj, change, index, is_template):
        "Helper function to generate formsets for add/change_view."
        formsets = []
        inline_instances = []
        prefixes = defaultdict(int)
        get_formsets_args = [request]
        if change:
            get_formsets_args.append(obj)
        base_prefix = self.get_formset(request).get_default_prefix()
        for FormSet, inline in self.get_formsets_with_inlines(
                *get_formsets_args):
            prefix = base_prefix + '-' + FormSet.get_default_prefix()
            if not is_template:
                prefix += '-%s' % index
            prefixes[prefix] += 1
            if prefixes[prefix] != 1 or not prefix:
                prefix = "%s-%s" % (prefix, prefixes[prefix])
            formset_params = {
                'instance': obj,
                'prefix': prefix,
                'queryset': inline.get_queryset(request),
            }
            if request.method == 'POST':
                formset_params.update({
                    'data': request.POST,
                    'files': request.FILES,
                    'save_as_new': '_saveasnew' in request.POST
                })
            formset = FormSet(**formset_params)
            formset.has_parent = True
            formsets.append(formset)
            inline_instances.append(inline)
        return formsets, inline_instances