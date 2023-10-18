def display(annotation, meta=True, **kwargs):
    '''Visualize a jams annotation through mir_eval

    Parameters
    ----------
    annotation : jams.Annotation
        The annotation to display

    meta : bool
        If `True`, include annotation metadata in the figure

    kwargs
        Additional keyword arguments to mir_eval.display functions

    Returns
    -------
    ax
        Axis handles for the new display

    Raises
    ------
    NamespaceError
        If the annotation cannot be visualized
    '''

    for namespace, func in six.iteritems(VIZ_MAPPING):
        try:
            ann = coerce_annotation(annotation, namespace)

            axes = func(ann, **kwargs)

            # Title should correspond to original namespace, not the coerced version
            axes.set_title(annotation.namespace)
            if meta:
                description = pprint_jobject(annotation.annotation_metadata, indent=2)

                anchored_box = AnchoredText(description.strip('\n'),
                                            loc=2,
                                            frameon=True,
                                            bbox_to_anchor=(1.02, 1.0),
                                            bbox_transform=axes.transAxes,
                                            borderpad=0.0)
                axes.add_artist(anchored_box)

                axes.figure.subplots_adjust(right=0.8)

            return axes
        except NamespaceError:
            pass

    raise NamespaceError('Unable to visualize annotation of namespace="{:s}"'
                         .format(annotation.namespace))