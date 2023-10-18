def mutate_list_of_nodes(node, context):
    """
    :type context: Context
    """

    return_annotation_started = False

    for child_node in node.children:

        if child_node.type == 'operator' and child_node.value == '->':
            return_annotation_started = True

        if return_annotation_started and child_node.type == 'operator' and child_node.value == ':':
            return_annotation_started = False

        if return_annotation_started:
            continue

        mutate_node(child_node, context=context)

        # this is just an optimization to stop early
        if context.number_of_performed_mutations and context.mutation_id != ALL:
            return