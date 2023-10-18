def bake(binder, recipe_id, publisher, message, cursor):
    """Given a `Binder` as `binder`, bake the contents and
    persist those changes alongside the published content.

    """
    recipe = _get_recipe(recipe_id, cursor)
    includes = _formatter_callback_factory()
    binder = collate_models(binder, ruleset=recipe, includes=includes)

    def flatten_filter(model):
        return (isinstance(model, cnxepub.CompositeDocument) or
                (isinstance(model, cnxepub.Binder) and
                 model.metadata.get('type') == 'composite-chapter'))

    def only_documents_filter(model):
        return isinstance(model, cnxepub.Document) \
            and not isinstance(model, cnxepub.CompositeDocument)

    for doc in cnxepub.flatten_to(binder, flatten_filter):
        publish_composite_model(cursor, doc, binder, publisher, message)

    for doc in cnxepub.flatten_to(binder, only_documents_filter):
        publish_collated_document(cursor, doc, binder)

    tree = cnxepub.model_to_tree(binder)
    publish_collated_tree(cursor, tree)

    return []